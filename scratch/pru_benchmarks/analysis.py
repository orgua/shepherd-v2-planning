import logging
import os
from pathlib import Path
from sys import stdout

import numpy as np

logger = logging.getLogger("Logic")
logger.addHandler(logging.StreamHandler(stream=stdout))
logger.setLevel(logging.DEBUG)


def get_files(
    start_path: Path,
    stem: str = "",
    suffix: str = ".log",
    recursion_depth: int = 0,
) -> list[Path]:
    if recursion_depth == 0:
        suffix = suffix.lower().split(".")[-1]
    dir_items = os.scandir(start_path)
    recursion_depth += 1
    files = []

    for item in dir_items:
        if item.is_dir():
            files += get_files(item.path, stem, suffix, recursion_depth)
            continue
        item_name = str(item.name).lower()
        item_ext = item_name.split(".")[-1]
        if item_ext == suffix and item_ext != item_name and stem in item_name:
            files.append(Path(item.path))
        if suffix == "" and item_ext == item_name:
            files.append(Path(item.path))
    if recursion_depth == 1 and len(files) > 0:
        logger.debug(" -> got %s files with the suffix '%s'", len(files), suffix)
    return files


class LogicAnalyze:
    """Analyzer for Saleae Logic CSV files."""

    def __init__(
        self,
        content: Path | np.ndarray,
    ) -> None:
        """Provide a file with two columns.

        - timestamp (seconds with fraction) and signal (can be analog).
        - class-parameters that are None (above) get auto-detected
          (some detectors still missing)
        """
        if isinstance(content, Path):
            self.events_sig: np.ndarray = np.loadtxt(
                content.as_posix(),
                delimiter=",",
                skiprows=1,
            )
            # TODO: if float fails load as str -
            #  cast first col as np.datetime64 with ns-resolution, convert to delta
        else:
            self.events_sig = content

        # verify table
        if self.events_sig.shape[1] != 2:
            raise TypeError(
                "Input file should have 2 rows -> (comma-separated) timestamp & value",
            )
        if self.events_sig.shape[0] < 8:
            raise TypeError("Input file is too short (< state-changes)")
        # verify timestamps
        time_steps = self.events_sig[1:, 0] - self.events_sig[:-1, 0]
        if any(time_steps < 0):
            raise TypeError("Timestamps are not continuous")

        # prepare samples & process params (order is important)
        self._convert_analog2digital()
        self._filter_redundant_states()
        self._add_duration()

    def _convert_analog2digital(self, *, invert: bool = False) -> None:
        """Divide dimension in two, divided by mean-value."""
        data = self.events_sig[:, 1]
        mean = np.mean(data)
        if invert:
            self.events_sig[:, 1] = data <= mean
        else:
            self.events_sig[:, 1] = data >= mean

    def _filter_redundant_states(self) -> None:
        """Sum of two sequential states is always 1 (True + False) if alternating."""
        data_0 = self.events_sig[:, 1]
        data_1 = np.concatenate([[not data_0[0]], data_0[:-1]])
        data_f = data_0 + data_1
        self.events_sig = self.events_sig[data_f == 1]

        if len(data_0) > len(self.events_sig):
            logger.debug(
                "filtered out %d/%d events (redundant)",
                len(data_0) - len(self.events_sig),
                len(data_0),
            )

    def _add_duration(self) -> None:
        """Calculate third column, duration of state in [baud-ticks]."""
        if self.events_sig.shape[1] > 2:
            logger.warning("Tried to add state-duration, but it seems already present")
            return

        dur_steps = self.events_sig[1:, 0] - self.events_sig[:-1, 0]
        dur_steps = np.reshape(dur_steps, (dur_steps.size, 1))
        self.events_sig = np.append(self.events_sig[:-1, :], dur_steps, axis=1)

    def get_state_stats(self, *, state: bool) -> None:
        states = (self.events_sig[:, 1] > 0.5) if state else (self.events_sig[:, 1] <= 0.5)

        durations = self.events_sig[states, 2]
        smin = round(durations.min() * 1e9)
        smax = round(durations.max() * 1e9)
        smea = round(durations.mean() * 1e9)
        logger.info(
            "State %s was enabled \tmin=%d, mean=%d, max=%d [ns]",
            state,
            smin,
            smea,
            smax,
        )
        # TODO: allow grouping by duration

    def histogram(self) -> None:
        pass
        # https://numpy.org/doc/stable/reference/generated/numpy.histogram.html


if __name__ == "__main__":
    path_here = Path(__file__).parent.absolute()
    files_csv = get_files(path_here, suffix=".csv")
    for file in files_csv:
        logger.info("#### Processing %s", file.name)
        log = LogicAnalyze(file)
        log.get_state_stats(state=True)
        log.get_state_stats(state=False)

    logger.info("finito")
