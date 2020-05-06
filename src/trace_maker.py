from src.full_trace import Trace
from src.schedule_types import Condition, State, ScheduleElement, schedule_from_dict
from typing import List

import os
import json
import random


class TraceMaker():
    """
    This class generates random trace based on the given schedule
    Args:
        - schedule: path to the existing schedule file
        - trace: path to the file where the trace should be stored
    """

    def __init__(self, schedule: str, trace: str, start_day: int = 0, duration: int = 14):
        self._schedule_path: str = schedule
        self._trace_path: str = trace
        self._trace: Trace = Trace()
        self._schedule: List[ScheduleElement]
        self._start_day = start_day
        self._duration = duration

        self.parse_schedule()

    def parse_schedule(self) -> None:
        'From the schedule file, creates a list of ScheduleElements'
        if os.path.exists(self._schedule_path):
            with open(self._schedule_path, 'r') as f:
                data = json.loads(f.read())
                self._schedule = schedule_from_dict(data)
        else:
            raise FileNotFoundError("Schedule file not found!")

    def generate_trace(self):
        """
        Iterates over all the ScheduleElements and generates events based on them.
        The events are added to the trace, which is then written to disk.
        """
        for element in self._schedule:
            if element.elem_type == 'one_shot':
                for i, day in enumerate(range(self._start_day, self._start_day + self._duration)):
                    if (element.condition.days == 7) or ((day % 7) in element.condition.days):
                        min_time = self.to_time(element.condition.time_start)
                        max_time = self.to_time(element.condition.time_end)
                        trigger_time = random.randint(min_time, max_time) + i * 1440
                        self._trace.add_event(trigger_time, element.event, element.target)
            elif element.elem_type == "multi_state":
                # TODO
                pass
            elif element.elem_type == "periodic_change":
                # TODO
                pass

    @staticmethod
    def to_time(time: str) -> int:
        'Convert time in "HH:MM" format to minutes'
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        return hour * 60 + mins
