from src.event import Event
from typing import List

import os


class Trace():
    """
    Complete event trace used by the scheduler

    Can be setup by either loading a dumped trace file, or by inserting events
    """

    def __init__(self):
        self._events: List[Event] = []

    @property
    def event_number(self) -> int:
        return len(self._events)

    @property
    def events(self) -> List[Event]:
        return self._events

    def event(self, index: int) -> Event:
        return self._events[index]

    def load_file(self, path: str) -> None:
        'Initializes the trace by reading the given file'
        if os.path.exists(path):
            with open(path, 'r') as f:
                lines: List[str] = f.readlines()
            for line in lines:
                # Initialize and store the event
                event: Event = Event(buffer=line)
                self._events.append(event)
        else:
            raise FileNotFoundError

    def store_file(self, path: str, overwrite: bool = False) -> None:
        'Writes its events to the given path'
        if os.path.exists(path) and not overwrite:
            raise FileExistsError
        else:
            lines: List[str] = []
            for event in self._events:
                line = repr(event)
                lines.append(line)
            with open(path, 'w') as f:
                f.writelines("\n".join(lines))

    def add_event(self, timestamp: int, value: str, target: str) -> None:
        """
        Creates and inserts a new event from the
        given args at the correct place
        """
        event = Event(timestamp, value, target)
        l: int = self.event_number
        i: int = 0
        while i < l and self._events[i].ts < timestamp:
            i += 1
        self._events.insert(i, event)
