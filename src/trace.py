from event import Event
from typing import List

import os


class Trace():
    def __init__(self):
        self._events: List[Event]
        # TODO

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
                event: Event = Event()
                event.deserialize(line)
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
                line = event.serialize()
                lines.append(line)
            with open(path, 'w') as f:
                f.writelines(lines)

    def add_event(self) -> None:
        """
        Creates and inserts a new event from the
        given args at the correct place
        """
        # TODO
        # Insert the event at the correct timestamp to keep the list ordered
        pass
