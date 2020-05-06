from full_trace import Trace


class Scheduler():
    """
    Event-driven scheduler. Uses an event trace to fire events.

    Args:
        - trace: path the the trace event file to use
    """

    def __init__(self, trace: str):
        self._trace_path: str = trace
        self._trace: Trace = Trace()
        self._trace.load_file(self._trace_path)

    def start(self):
        'Starts the scheduler'
        # TODO
        pass
