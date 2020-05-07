from src.full_trace import Trace
from src.schedule_types import State, ScheduleElement, schedule_from_dict
from typing import List, Dict, Tuple

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
                for i, day in enumerate(range(self._start_day, self._start_day + self._duration)):
                    if (element.condition.days == 7) or ((day % 7) in element.condition.days):
                        print("ye")
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
                events_number = math.ceil((self._duration + 1440) / element.update_period)
                states_dict: Dict[int, int] = {}
                events_list: List[Tuple[int, str]] = []
                for i in range(events_number):
                    ts = i * element.update_period
                    prev_state_ts, prev_state_val = self.get_prev_state(states_dict, element, ts)
                    next_state_ts, next_state_val = self.get_next_state(states_dict, element, ts)
                    val = str(prev_state_val + (next_state_val - prev_state_val) * (ts - prev_state_ts) / (next_state_ts - prev_state_ts))
                    events_list.append((ts, val))
                    # TODO: add the correct events to the trace

    def get_prev_state(self, states_dict: dict, element: ScheduleElement, ts: int) -> Tuple[int, int]:
        states_ts: Dict[int, Tuple[int, int]] = {self.to_time(i.time): (i.min_value, i.max_value) for i in element.states}
        if ts in states_dict.keys():
            return ts, states_dict[ts]
        elif ts % 1440 in states_ts:
            # Generate a new data point and store it in the dict
            state = states_ts[ts % 1440]
            val = random.randint(state[0], state[1])
            states_dict[ts] = val
            return ts, val
        else:
            # Find the oldest previous state and return it
            prev_ts = -1
            prev_val = 0
            changed = False
            for state_ts in states_dict.keys():
                if state_ts < ts and state_ts > prev_ts:
                    prev_ts = state_ts
                    prev_val = states_dict[state_ts]
                    changed = True
                if changed:
                    return prev_ts, prev_val
                else:
                    # Generate a new point

        return - 1, -1

    def get_next_state(self, states_dict: dict, element: ScheduleElement, ts: int) -> Tuple[int, int]:
        states_ts: Dict[int, Tuple[int, int]] = {self.to_time(i.time): (i.min_value, i.max_value) for i in element.states}
        if ts in states_dict.keys():
            return ts, states_dict[ts]
        elif ts % 1440 in states_ts:
            # Generate a new data point and store it in the dict
            state = states_ts[ts % 1440]
            val = random.randint(state[0], state[1])
            states_dict[ts] = val
            return ts, val
        else:
            # Find the oldest previous state and return it
            prev_ts = -1
            prev_val = 0
            for state_ts in states_dict.keys():
                if state_ts > ts and state_ts < prev_ts:
                    prev_ts = state_ts
                    prev_val = states_dict[state_ts]
                return prev_ts, prev_val
        return -1, -1

    def write_trace(self, overwrite: bool = False):
        "Dump the generated event trace to a file"
        self._trace.store_file(self._trace_path, overwrite=overwrite)

    @staticmethod
    def to_time(time: str) -> int:
        'Convert time in "HH:MM" format to minutes'
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        return hour * 60 + mins
