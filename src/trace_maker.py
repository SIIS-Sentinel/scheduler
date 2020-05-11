from src.full_trace import Trace
from src.schedule_types import State, ScheduleElement, schedule_from_dict
from typing import List, Dict, Tuple, Optional

import os
import json
import random
import math


class TraceMaker():
    """
    This class generates random trace based on the given schedule
    Args:
        - schedule: path to the existing schedule file
        - trace: path to the file where the trace should be stored
        - start_day: day of the week when the trace should start (Mon=0)
        - duration: number of days the trace should last
    """

    def __init__(self, schedule: str, trace: str, start_day: int = 0, duration: int = 14):
        self._schedule_path: str = schedule
        self._trace_path: str = trace
        self._trace: Trace = Trace()
        self._schedule: List[ScheduleElement]
        self._start_day = start_day
        self._duration = duration

        self.parse_schedule()

    @property
    def _start_time(self) -> int:
        return self._start_day * 1440

    @property
    def _duration_min(self) -> int:
        return self._duration * 1440

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
                    if (7 in element.condition.days) or ((day % 7) in element.condition.days):
                        min_time = self.to_time(element.condition.time_start)
                        max_time = self.to_time(element.condition.time_end)
                        trigger_time = random.randint(min_time, max_time) + i * 1440
                        self._trace.add_event(trigger_time, element.event, element.target)
            elif element.elem_type == "multi_state":
                for i, day in enumerate(range(self._start_day, self._start_day + self._duration)):
                    if (7 in element.condition.days) or ((day % 7) in element.condition.days):
                        time = self.to_time(element.condition.time_start)
                        end_time = self.to_time(element.condition.time_end)
                        max_duration = end_time - time
                        state: State = None
                        while time <= end_time:
                            # Pick a new state and duration at random
                            state = random.choice(element.states)
                            min_duration = state.min_duration
                            max_duration = state.max_duration
                            duration = min(random.randint(min_duration, max_duration), max_duration)
                            trigger_time = time + i * 1440
                            # Add to the trace
                            self._trace.add_event(trigger_time, state.event, element.target)
                            # Update the remaining time
                            time += duration
                            max_duration = end_time - time

            elif element.elem_type == "periodic_change":
                # Generate dict of target values
                targets: Dict[int, int] = {}
                for day in range(self._start_day - 1, self._start_day + self._duration + 1):
                    for state in element.states:
                        ts = self.to_time(state.time) + day * 1440
                        val = random.randint(state.min_value, state.max_value)
                        targets[ts] = val
                # Create events list L, calculate number of events
                events: List[Tuple[int, int]] = []
                events_number: int = math.ceil(self._duration_min / element.update_period) + 1
                # Iterate over all events numbers
                for i in range(events_number):
                    event_ts: int = i * element.update_period + self._start_time
                    # Calculate their value and add them to L
                    if event_ts in targets.keys():
                        event_val = targets[event_ts]
                    else:
                        prev: Tuple[int, int] = self.get_prev_ts(event_ts, targets)
                        next: Tuple[int, int] = self.get_next_ts(event_ts, targets)
                        event_val: int = self.interpolate(event_ts, prev, next)
                    events.append((event_ts, event_val))

                # For each element of L, check if their ts match the condition
                last_value: int = None
                for event in events:
                    event_day = (math.floor(event[0] / 1440)) % 7
                    if (7 in element.condition.days) or (event_day in element.condition.days):
                        # Only add the event if it changes the previous value
                        if last_value is None or event[1] != last_value:
                            self._trace.add_event(event[0], str(event[1]), element.target)
                        last_value = event[1]

    def write_trace(self, overwrite: bool = False):
        "Dump the generated event trace to a file"
        self._trace.store_file(self._trace_path, overwrite=overwrite)

    @staticmethod
    def get_prev_ts(ts: int, points: Dict[int, int]) -> Tuple[int, int]:
        best_ts: Optional[int] = None
        best_val: Optional[int] = None
        for point in points:
            if (best_ts is None or point > best_ts) and point < ts:
                best_ts = point
                best_val = points[point]
        if best_ts is None or best_val is None:
            raise KeyError(f"Previous value of {ts} not found.")
        else:
            return (best_ts, best_val)

    @staticmethod
    def get_next_ts(ts: int, points: Dict[int, int]) -> Tuple[int, int]:
        best_ts: Optional[int] = None
        best_val: Optional[int] = None
        for point in points:
            if (best_ts is None or point < best_ts) and point > ts:
                # raise Exception(f"{point} and {best_ts} and {ts}")
                best_ts = point
                best_val = points[point]
        if best_ts is None or best_val is None:
            raise KeyError(f"Next value of {ts} not found.")
        else:
            return (best_ts, best_val)

    @staticmethod
    def interpolate(x: int, prev: Tuple[int, int], next: Tuple[int, int]) -> int:
        "Performs a linear interpolation between prev and next at the x-value x"
        slope: float = (x - prev[0]) / (next[0] - prev[0])
        y: float = prev[1] + (next[1] - prev[1]) * slope
        return int(round(y, 0))

    @staticmethod
    def to_time(time: str) -> int:
        'Convert time in "HH:MM" format to minutes'
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        return hour * 60 + mins
