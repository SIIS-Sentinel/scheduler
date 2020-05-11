from src.full_trace import Trace
from src.scheduler_config import SchedulerConfig

import paho.mqtt.client as mqtt
import json
import sched
import time


class Scheduler():
    """
    Event-driven scheduler. Uses an event trace to fire events.

    Args:
        - trace: path the the trace event file to use
    """

    def __init__(self, trace_path: str, config_path: str):
        self._trace: Trace = Trace()
        self._start_time: int
        self._trace.load_file(trace_path)
        self._cfg: SchedulerConfig = self.load_config(config_path)
        self._client: mqtt.Client = mqtt.Client(self._cfg.name)
        self._engine: sched.scheduler = sched.scheduler(self.scheduler_time, self.scheduler_sleep)

        self.configure_client()

    @staticmethod
    def load_config(config_path: str) -> SchedulerConfig:
        with open(config_path, 'r') as f:
            data = json.loads(f.read())
            return SchedulerConfig.from_dict(data)

    @staticmethod
    def connected():
        print("Connected to broker")

    @staticmethod
    def scheduler_sleep(delay: int) -> None:
        "Delays for the given number of minutes"
        delay_s: int = delay * 60
        time.sleep(delay_s)

    def configure_client(self) -> None:
        self._client.on_connect(self.connected)
        self._client.username_pw_set(self._cfg.username, self._cfg.password)
        self._client.connect(self._cfg.addr, self._cfg.port)
        self._client.loop_start()

    def scheduler_time(self) -> int:
        "Returns the number of minutes since the scheduler started"
        real_time: int = int(time.time() // 60)
        return real_time - self._start_time

    def start(self) -> None:
        'Starts the scheduler'
        self._start_time = int(time.time() // 60)
        for event in self._trace.events:
            self._engine.enterabs(event.ts, 0, self.execute_event, argument=(event.value, event.target))

    def execute_event(self, value: str, target: str) -> None:
        print(f"Sending value {value} to target {target}")
        self._client.publish(target, payload=value, qos=1, retain=False)
