import logging
import sys
import threading
import time

import chromalog
import numpy as np

# TODO: try odd buffer sizes

config: dict[str, int] = {
    "timestep_writer": 0.100,  # seconds
    "timestep_reader": 0.010,
    "timestep_cache": 0.100,
    "timestep_super": 1.200,
    "buffer_size": 1024,  # n
    "cache_size": 128,
    "block_size": 16,
    "write_count": 2 * 1024 + 256,
}

enable_cache: bool = True  # reader will warn when reading uncached values (but it will work)
IDX_OUT_OF_BOUND: int = 0xFFFFFFFF

# Top-Level Package-logger
log = logging.getLogger("Shp")
log.setLevel(logging.DEBUG)
log.propagate = 0

# handler for CLI
console_handler = chromalog.ColorizingStreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)


class DataBuffer:
    def __init__(self) -> None:
        self.idx_reader: int = IDX_OUT_OF_BOUND  # position of next (not yet read) value
        self.idx_writer: int = IDX_OUT_OF_BOUND  # position of next (not yet written) value
        self.data = np.zeros(shape=config["buffer_size"], dtype=np.uint32)
        self.BLOCKS: int = config["buffer_size"] // config["block_size"]
        self.run_writer: bool = True
        self.run_reader: bool = False


class DataCache:
    def __init__(self) -> None:
        self.data = np.zeros(shape=config["cache_size"], dtype=np.uint32)
        self.flags = np.zeros(shape=config["buffer_size"] // config["block_size"])
        self.BLOCKS: int = config["cache_size"] // config["block_size"]


class Cache(threading.Thread):
    def __init__(self, buffer: DataBuffer, cache: DataCache) -> None:
        threading.Thread.__init__(self)
        self._buffer = buffer
        self._cache = cache
        self._block_idx_head: int = IDX_OUT_OF_BOUND // config["block_size"]
        self._block_idx_tail: int = IDX_OUT_OF_BOUND // config["block_size"]
        self._block_fill: int = 0

    def run(self) -> None:
        log.debug("[cache] waiting to start")
        while not self._buffer.run_writer:
            time.sleep(config["timestep_cache"])
        log.info("[cache] started")
        while self._buffer.run_writer or self._buffer.run_reader:
            self.update()
            time.sleep(config["timestep_cache"])
        log.info("[cache] stopped")

    def update(self) -> None:
        if self._buffer.idx_writer >= config["buffer_size"]:
            return

        idx_read: int = self._buffer.idx_reader // config["block_size"]
        idx_write: int = self._buffer.idx_writer // config["block_size"]

        if (idx_read != self._block_idx_tail) and (self._block_fill > 0):
            self._block_fill -= self._remove(self._block_idx_tail)
            self._block_idx_tail += 1
            if self._block_idx_tail >= self._buffer.BLOCKS:
                self._block_idx_tail = 0

        if self._block_fill >= self._cache.BLOCKS:
            return

        head_next: int = self._block_idx_head + 1
        if head_next >= self._buffer.BLOCKS:
            head_next = 0
        if head_next != idx_write:
            self._block_fill += self._add(head_next)
            self._block_idx_head = head_next

    def _add(self, block_idx: int) -> int:
        if block_idx >= self._buffer.BLOCKS:
            return 0
        cache_offset: int = (block_idx * config["block_size"]) % config["cache_size"]
        buffer_offset: int = (block_idx * config["block_size"]) % config["buffer_size"]
        self._cache.data[cache_offset : cache_offset + config["block_size"]] = self._buffer.data[
            buffer_offset : buffer_offset + config["block_size"]
        ]
        self._cache.flags[block_idx] = 1
        log.debug(f"[cache] cached block {block_idx}, fill = {self._block_fill + 1}")
        return 1

    def _remove(self, block_idx: int) -> int:
        if block_idx >= self._buffer.BLOCKS:
            return 0
        self._cache.flags[block_idx] = 0
        cache_offset: int = (block_idx * config["block_size"]) % config["cache_size"]
        self._cache.data[cache_offset : cache_offset + config["block_size"]] = 0
        if self._block_fill < self._cache.BLOCKS:
            log.debug(f"[cache] cleared block {block_idx}, fill = {self._block_fill + 1}")
        return 1


class Writer(threading.Thread):
    def __init__(self, buffer: DataBuffer) -> None:
        threading.Thread.__init__(self)
        self._buffer: DataBuffer = buffer
        self._counter: int = 0  # to end primary TX

    def run(self) -> None:
        log.debug("[writer] waiting to start")
        while not self._buffer.run_writer:
            time.sleep(config["timestep_writer"])
        log.info("[writer] started")
        while self.write_block():
            time.sleep(config["timestep_writer"])
        log.info("[writer] filled buffer, will start reader")
        self._buffer.run_reader = True
        while self._counter < config["write_count"]:
            self.write_block()
            time.sleep(config["timestep_writer"])
        self._buffer.run_writer = False
        log.info("[writer] finished transmission -> will stop now!")

    def get_free_space(self) -> int:
        if self._buffer.idx_writer == IDX_OUT_OF_BOUND:
            return config["buffer_size"]
        if self._buffer.idx_reader == IDX_OUT_OF_BOUND:
            return (config["buffer_size"] - self._buffer.idx_writer) % config["buffer_size"]
        return (self._buffer.idx_reader - self._buffer.idx_writer) % config["buffer_size"]

    def write_block(self) -> bool:
        to_write = self.get_free_space()
        if to_write < config["block_size"]:
            return False
        if self._buffer.idx_writer == IDX_OUT_OF_BOUND:
            self._buffer.idx_writer = 0
        block_idx = self._buffer.idx_writer // config["block_size"]
        for _ in range(config["block_size"]):
            self._buffer.data[self._buffer.idx_writer] = self._counter
            self._buffer.idx_writer = (self._buffer.idx_writer + 1) % config["buffer_size"]
            self._counter += 1
        log.debug(f"[writer] filled block {block_idx}")
        return True


class Reader(threading.Thread):
    def __init__(self, buffer: DataBuffer, cache: DataCache) -> None:
        threading.Thread.__init__(self)
        self._buffer: DataBuffer = buffer
        self._cache: DataCache = cache
        self._sample_last: int | None = None

    def run(self) -> None:
        log.debug("[reader] waiting to start")
        while not self._buffer.run_reader:
            # wait for start
            time.sleep(config["timestep_reader"])
        log.info("[reader] started")
        while self._buffer.run_reader:
            value = self.read_sample()
            if (self._sample_last is not None) and (value != self._sample_last + 1):
                raise ValueError(
                    "[reader] value not as expected (%d != %d + 1)", value, self._sample_last
                )
            self._sample_last = value
            if ((self._buffer.idx_reader) + 1 % config["buffer_size"]) == self._buffer.idx_writer:
                log.info("[reader] did run dry - will end now")
                self._buffer.run_reader = False
            time.sleep(config["timestep_reader"])
        log.info("[reader] stopped")

    def read_sample(self) -> int:
        if self._buffer.idx_reader == IDX_OUT_OF_BOUND:
            self._buffer.idx_reader = 0

        block_idx = self._buffer.idx_reader // config["block_size"]
        if self._cache.flags[block_idx]:
            idx_cache: int = self._buffer.idx_reader % config["cache_size"]
            value = self._cache.data[idx_cache]
        else:
            value = self._buffer.data[self._buffer.idx_reader]
            log.warning("[reader] idx %d was not cached", self._buffer.idx_reader)

        self._buffer.idx_reader = (self._buffer.idx_reader + 1) % config["buffer_size"]
        return value


if __name__ == "__main__":
    data_buffer = DataBuffer()
    data_cache = DataCache()

    dev_a = Reader(data_buffer, data_cache)
    dev_b = Writer(data_buffer)
    dev_c = Cache(data_buffer, data_cache)

    dev_a.start()
    dev_b.start()
    if enable_cache:
        dev_c.start()

    dev_a.join()
    dev_b.join()
    if enable_cache:
        dev_c.join()
