from scheduler.scheduler_config import SchedulerConfig
from scheduler.full_trace import Trace


import paho.mqtt.client as mqtt
import json
import sched
import time
import os

from intruder.intruder_hub import IntruderHub


class Scheduler():
    """
    Event-driven scheduler. Uses an event trace to fire events.

    Args:
        - trace: path the the trace event file to use
    """

    def __init__(self, trace_path: str, config_path: str, debug: bool = False):
        self._trace: Trace = Trace()
        self._start_time: float
        self._trace.load_file(trace_path)
        self._debug: bool = debug
        self._cfg: SchedulerConfig = self.load_config(config_path)
        self._client: mqtt.Client = mqtt.Client(self._cfg.name)
        if not self._debug:
            self.configure_client()
        self._engine: sched.scheduler = sched.scheduler(
            self.scheduler_time,
            self.scheduler_sleep
        )
        if os.path.exists(self._cfg.log_path) and not self._cfg.overwrite_log:
            raise FileExistsError(
                "Log file already exists and no overwrite configured")

        # Intruder module
        self.intruder: IntruderHub = IntruderHub(self._cfg.name, self._client)

        # Connect to broker
        if not self._debug:
            self.connect()

    @staticmethod
    def load_config(config_path: str) -> SchedulerConfig:
        with open(config_path, 'r') as f:
            data = json.loads(f.read())
            return SchedulerConfig.from_dict(data)

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print("Connected to MQTT broker")
        self.intruder.on_connect(client, userdata, flags, rc)

    def on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        self.intruder.on_message(client, userdata, message)

    @staticmethod
    def scheduler_sleep(delay: float) -> None:
        "Delays for the given number of minutes"
        delay_s: float = delay * 60
        time.sleep(delay_s)

    def configure_client(self) -> None:
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.tls_set(ca_certs=self._cfg.cafile,
                             certfile=self._cfg.certfile,
                             keyfile=self._cfg.keyfile)

    def connect(self) -> None:
        self._client.connect(self._cfg.addr, self._cfg.port)
        self._client.loop_start()

    def scheduler_time(self) -> float:
        "Returns the number of minutes since the scheduler started"
        real_time: float = time.time() / 60
        return real_time - self._start_time

    def start(self) -> None:
        'Starts the scheduler'
        while not self._debug and not self._client.is_connected():
            time.sleep(0.1)
        # Wait until the start of a minute
        time.sleep(60 - (time.time() % 60))
        self._start_time = time.time() // 60
        for event in self._trace.events:
            self._engine.enterabs(
                event.ts, 0, self.execute_event, argument=(event.value, event.target))
        print("Starting the scheduling engine")
        self._engine.run()
        print("All events have been dispatched")

    def execute_event(self, value: str, target: str) -> None:
        print(f"Sending value {value} to target {target}")
        if not self._debug:
            self._client.publish(target, payload=value, qos=1, retain=False)
        with open(self._cfg.log_path, "a") as f:
            log_entry: str = f"{time.time()}, {target}, {value}"
            f.write(log_entry)
        print("Value sent")


if __name__ == "__main__":
    s = Scheduler("tests/files/test_trace.txt",
                  "files/scheduler_config.json")
    s.start()
