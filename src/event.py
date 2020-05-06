import ast


class Event():
    """
    Scheduler event, characterized by a timestamp, a value, and a target

    Can be instantiated either with explicit values, or with a repr of another Event
    """

    def __init__(self, timestamp: int = None, value: str = None, target: str = None, buffer: str = None):
        if buffer is not None:
            self._deserialize(buffer)
        elif timestamp is None or value is None or target is None:
            self._ts: int = 0
            self._value: str = ""
            self._target: str = ""
        else:
            self._ts = timestamp
            self._value = value
            self._target = target

    def __repr__(self) -> str:
        'Returns a serialized version of itself for writing to a file'
        data: dict = {
            "ts": self._ts,
            "value": self._value,
            "target": self._target
        }
        return repr(data)

    def _deserialize(self, buf: str) -> None:
        ' Initializes the event from the given buffer'
        data = ast.literal_eval(buf)
        self._ts = data["ts"]
        self._value = data["value"]
        self._target = data["target"]

    @property
    def ts(self) -> int:
        return self._ts

    @property
    def value(self) -> str:
        return self._value

    @property
    def target(self) -> str:
        return self._target
