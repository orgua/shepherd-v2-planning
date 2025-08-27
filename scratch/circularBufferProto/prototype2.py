import random
import sys
import threading
from typing import Any

# writing and reading pointers
writing_ts_py: int = 0
reading_ts_pru: int = 0

# access to the buffer
access: str = "PY_W"

# list of data supervised by the supervisor thread
data_written = []
data_processed = []
data_read = []


class RingBuffer:
    """Ring-buffer that manages itself (hold data, indices, locks, )."""

    def __init__(self, capacity: int) -> None:
        self.buffer: list[Any] = [None] * capacity
        self.capacity = capacity
        self.write_size = 0
        self.read_size = 0
        self.write_index = 0
        self.read_index = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def append(self, value: Any) -> None:
        with self.lock:
            self.buffer[self.write_index] = value
            self.write_index = (self.write_index + 1) % self.capacity
            if self.write_size < self.capacity:
                self.write_size += 1

            self.condition.notify_all()

    def get(self) -> Any:
        with self.lock:
            value = self.buffer[self.read_index]
            self.read_index = (self.read_index + 1) % self.capacity

            if self.read_size < self.capacity:
                self.read_size += 1

            self.condition.notify_all()
            return value

    def isFull(self) -> bool:
        if self.write_size == self.capacity:
            self.write_size = 0
            return True
        return False

    def isEmpty(self) -> bool:
        if self.read_size == self.capacity:
            self.read_size = 0
            return True
        return False


class WriteByPython(threading.Thread):
    """Writer-Implementation that mimics the python-side of the beaglebone."""

    def __init__(self, buffer: RingBuffer) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self) -> None:
        global access
        global writing_ts_py
        while True:
            if access == "PY_W":
                data: list[int] = random.sample(range(1, 5), 2)
                writing_ts_py = self.buffer.write_index
                result = [(writing_ts_py, x) for x in data]
                self.buffer.append(result)
                data_written.append(result)
                if buffer.isFull():
                    access = "PRU_R"


class ReadByPru(threading.Thread):
    """Reader-Implementation that mimics the PRU-side of the beaglebone."""

    def __init__(self, buffer: RingBuffer) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self) -> None:
        while True:
            global access
            global reading_ts_pru
            if access == "PRU_R":
                reading_ts_pru = self.buffer.read_index
                values = self.buffer.get()
                processed_result = []
                for tuple_i in values:
                    processed_result.append((tuple_i[0], tuple_i[1] ** 2))

                    if False:
                        print(
                            f"[PRU]: read_index = \t {reading_ts_pru} and "
                            f"write_index = \t {self.buffer.write_index}"
                        )

                self.buffer.append(processed_result)
                data_processed.append(processed_result)

                if self.buffer.isEmpty() and self.buffer.isFull():
                    access = "PY_R"


class ReadByPython(threading.Thread):
    """Reader-Implementation that mimics the python-side of the beaglebone."""

    def __init__(self, buffer: RingBuffer) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self) -> None:
        global access
        while True:
            if access == "PY_R":
                values = self.buffer.get()
                data_read.append(values)
                # print("[Reading by Python]: Data read = \t",values)
                if self.buffer.isEmpty():
                    access = "PY_W"
                    # print("[Reading by Python]: read_index = \t",self.buffer.read_index)


class SupervisorThread(threading.Thread):
    """Separate supervising thread that monitors the Buffer."""

    def __init__(self, buffer: RingBuffer) -> None:
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.every_data = []

    def run(self) -> None:
        while True:
            if writing_ts_py < reading_ts_pru:
                print(
                    f"SupervisorThread] Error: "
                    f"The reading pointer{reading_ts_pru} exceeded the "
                    f"writing pointer {writing_ts_py}",
                )
                sys.exit()

            if data_read != data_processed and len(data_read) == len(data_processed):
                print(
                    "[SupervisorThread] Error: "
                    "Mismatch in data processed by PRU and data read by Python\n",
                )
                sys.exit()


if __name__ == "__main__":
    # Create the shared buffers
    buffer = RingBuffer(10)

    # Create the writer thread
    python_write = WriteByPython(buffer)
    python_write.start()

    # Create the reader thread
    pru_read = ReadByPru(buffer)
    pru_read.start()

    python_read = ReadByPython(buffer)
    python_read.start()

    # Create the supervisor thread
    supervisor = SupervisorThread(buffer)
    supervisor.start()

    # Wait for all threads to finish
    python_write.join()
    pru_read.join()
    python_read.join()
    supervisor.join()
