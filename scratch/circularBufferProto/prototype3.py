import random
import threading
import time
from copy import copy
from typing import Self

config: dict[str, int] = {
    "timestep_a": 0.100,  # seconds
    "timestep_b": 0.010,
    "timestep_s": 1.200,
    "samples_buffer": 17,  # n
    "samples_runtime": 500,
}

# TODO: play with config - try edge-cases (ts_a > samples_buffer * ts_b)


class DataStructure:
    def __init__(self, voltage: int = 0, current: int = 0) -> None:
        self.voltage = voltage
        self.current = current

    def __eq__(self, ds2: Self) -> bool:
        return (self.voltage == ds2.voltage) and (self.current == ds2.current)

    def __str__(self):
        return f"IV[{self.current}, {self.voltage}]"


class SharedMem:
    def __init__(self, size: int) -> None:
        self.data: list[DataStructure] = [DataStructure()] * size
        self.size = size
        self.timestamp: int = 0
        self.start_b: bool = False
        self.idx_b: int = -1  # negative for initial fill


class SupervisorMem:
    def __init__(self) -> None:
        self.data_a_in: list[DataStructure] = []
        self.data_a_out: list[DataStructure] = []
        self.data_b_in: list[DataStructure] = []
        self.data_b_out: list[DataStructure] = []
        self.counter_ab: int = 0
        self.counter_ba: int = 0
        self.run: bool = True

    def compare_a(self) -> bool:
        if len(self.data_a_out) and len(self.data_b_in):
            data_a = self.data_a_out.pop(0)
            data_b = self.data_b_in.pop(0)
            if data_a != data_b:
                raise ValueError(
                    f"[supervisor] AB-Mismatch - {data_a} != {data_b} (AB)",
                )
            self.counter_ab += 1
            return True
        return False

    def compare_b(self) -> bool:
        if len(self.data_b_out) and len(self.data_a_in):
            data_a = self.data_a_in.pop(0)
            data_b = self.data_b_out.pop(0)
            if data_a != data_b:
                raise ValueError(
                    f"[supervisor] BA-Mismatch - {data_b} != {data_a} (AB)",
                )
            self.counter_ab += 1
            return True
        return False

    def report(self) -> None:
        queue = [
            len(self.data_a_out),
            len(self.data_b_in),
            len(self.data_b_out),
            len(self.data_a_in),
        ]
        print(
            f"\t -> supervisor compared {[self.counter_ab, self.counter_ba]} (AB, BA) messages, "
            f"  -> fill of message-queues = {queue} (ABBA)",
        )


class Supervisor(threading.Thread):
    def __init__(self, buffer: SupervisorMem) -> None:
        threading.Thread.__init__(self)
        self.visor = buffer

    def run(self) -> None:
        print("[visor] started")
        while self.visor.run:
            self.check()
        self.check()  # final QA
        print("[visor] stopped")

    def check(self) -> None:
        time.sleep(config["timestep_s"])
        while self.visor.compare_a():
            continue
        while self.visor.compare_b():
            continue
        self.visor.report()


class DeviceA(threading.Thread):
    """TODO:
         - implement reading back from dev_b
         - "bug": dev_a writes more than configured

    shared-mem access stat:
        - start_b   -> written once
        - timestamp -> write once every bufferoverflow
        - data      -> write and read chunk-wise
        - idx_b     -> only read once every chunk of data written

        -> is this the optimal solution?
    """

    def __init__(self, buffer_data: SharedMem, buffer_s: SupervisorMem) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer_data
        self.visor = buffer_s
        self.idx_write: int = 0
        self.buffer_size = buffer_data.size  # read once
        self.counter: int = 0  # to end primary TX

    def run(self) -> None:
        print("[dev_a] started")
        self.read_and_write()
        print("[dev_a] filled buffer -> will start dev_b now!")
        self.buffer.start_b = True
        while self.counter < config["samples_runtime"]:
            self.read_and_write()
            time.sleep(config["timestep_a"])
        print("[dev_a] finished transmission -> will stop supervisor now!")
        self.visor.run = False
        print("[dev_a] stopped")

    def read_and_write(self) -> None:
        to_write = (self.buffer_size + self.buffer.idx_b - self.idx_write) % self.buffer_size
        for _ in range(to_write):
            if self.idx_write == 0:
                self.buffer.timestamp += 1
            # produce fake data
            ds = DataStructure(
                current=self.counter,
                voltage=random.sample(range(1, 2**20), 1),
            )
            self.buffer.data[self.idx_write] = copy(ds)
            self.idx_write = (self.idx_write + 1) % self.buffer_size
            self.counter += 1
            self.visor.data_a_out.append(copy(ds))


class DeviceB(threading.Thread):
    """shared-mem access stat:
    - start_b   -> read once after a reset
    - timestamp -> read once every bufferoverflow
    - data      -> read and write once every timestep
    - idx_b     -> only write once every timestep

    -> is this the optimal solution?
    """

    def __init__(self, buffer_data: SharedMem, buffer_s: SupervisorMem) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer_data
        self.visor = buffer_s
        self.idx_read: int = 0  # internal / fast
        self.buffer_size = buffer_data.size  # read once
        self.counter: int = 0  # just for verifying functionality
        self.timestamp_old: int = 0

    def run(self) -> None:
        print("[dev_b] waiting to start")
        while not self.buffer.start_b:
            # wait for start
            time.sleep(config["timestep_b"])
        print("[dev_b] started")
        while True:
            if self.idx_read == 0:
                if self.buffer.timestamp == self.timestamp_old:
                    print("[dev_b] will quit (no new ts found)")
                    break
                if self.buffer.timestamp == self.timestamp_old + 1:
                    self.timestamp_old = self.buffer.timestamp
                else:
                    raise ValueError(
                        f"[dev_b] timestamp unusual (expected {self.buffer.timestamp} == {self.timestamp_old} + 1)",
                    )

            self.read_and_write()
            time.sleep(config["timestep_b"])
        print("[dev_b] stopped")

    def read_and_write(self) -> None:
        dsi = self.buffer.data[self.idx_read]
        self.visor.data_b_in.append(copy(dsi))
        # produce fake data
        dso = DataStructure(
            current=self.counter,
            voltage=random.sample(range(1, 2**20), 1),
        )
        self.buffer.data[self.idx_read] = copy(dso)
        self.visor.data_b_out.append(copy(dso))
        self.buffer.idx_b = self.idx_read
        self.idx_read = (self.idx_read + 1) % self.buffer_size
        self.counter += 1


if __name__ == "__main__":
    data_b = SharedMem(config["samples_buffer"])
    data_s = SupervisorMem()

    dev_a = DeviceA(data_b, data_s)
    dev_b = DeviceB(data_b, data_s)
    dev_s = Supervisor(data_s)

    dev_s.start()
    dev_b.start()
    dev_a.start()

    dev_s.join()
    dev_b.join()
    dev_a.join()
