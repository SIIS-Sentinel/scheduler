from full_trace import Trace


class TraceMaker():
    """
    This class generates random trace based on the given schedule
    Args:
        - schedule: path to the existing schedule file
        - trace: path to the file where the trace should be stored
    """

    def __init__(self, schedule: str, trace: str):
        self._schedule_path: str = schedule
        self._trace_path: str = trace
        self._trace: Trace = Trace()

    @property
    def schedule(self):
        return self._schedule_path

    @schedule.setter
    def schedule(self, path: str):
        self._schedule_path = path

    @property
    def trace(self):
        return self._trace_path

    @trace.setter
    def trace(self, path: str):
        self._trace_path = path
