from trace import Trace


class Scheduler():
    def __init__(self, trace: str):
        self._trace_path: str = trace
        self._trace: Trace = Trace()
        self._trace.load_file(self._trace_path)

    def start(self):
        'Starts the scheduler'
        # TODO
        pass
