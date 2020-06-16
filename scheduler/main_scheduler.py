from scheduler.scheduler_config import SchedulerConfig
from scheduler.full_trace import Trace


import paho.mqtt.client as mqtt
import json
import sched
import time
import os

from intruder.intruder_hub import IntruderHub
from bookkeeper.sql import create_sessions, Node, Event


class Scheduler():
    """
    Event-driven scheduler. Uses an event trace to fire events.

    Args:
        - trace: path the the trace event file to use
    """

    def __init__(self, trace_path: str, config_path: str, debug: bool = False, db_path: str = None):
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

        # SQL session
        self.session = create_sessions(self._cfg.db_path)

        # Intruder module
        self.intruder: IntruderHub = IntruderHub(
            self._cfg.name, self._client, db_path=db_path)

        # Connect to broker
        if not self._debug:
            self.connect()

    @staticmethod
    def load_config(config_path: str) -> SchedulerConfig:
        with open(config_path, 'r') as f:
            data = json.loads(f.read())
            return SchedulerConfig.from_dict(data)

    def get_node_id(self, name: str) -> int:
        node = self.session.query(Node.id).filter_by(name=name).all()
        if len(node) == 0:
            return -1
        node_id: int = node[0].id
        return node_id

    def add_event(self, ts: float, event_type: str, node: str) -> None:
        node_id: int = self.get_node_id(node)
        if node_id == -1:
            print(f"Node {node} not found")
            raise Exception(f"Node {node} not found in the database")
        newEvent: Event = Event(event_type=event_type, timestamp=ts, node_id=node_id)
        self.session.add(newEvent)
        self.session.commit()

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print("Scheduler: Connected to MQTT broker")
        self.intruder.on_connect(client, userdata, flags, rc)

    def on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        # print(message.payload.decode())
        self.intruder.on_message(client, userdata, message)

    def on_log(self, client, userdata, level, buf):
        if level == mqtt.MQTT_LOG_WARNING:
            print("Warning: %s" % (buf))
        elif level == mqtt.MQTT_LOG_ERR:
            print("Error: %s" % (buf))
        else:
            print("Log: %s" % (buf))

    @staticmethod
    def scheduler_sleep(delay: float) -> None:
        "Delays for the given number of minutes"
        delay_s: float = delay * 60
        print(f"Sleeping for {delay_s}s")
        time.sleep(delay_s)

    def configure_client(self) -> None:
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.on_log = self.on_log
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
        if not self._debug:
            time.sleep(60 - (time.time() % 60))
        self._start_time = time.time() // 60
        for event in self._trace.events:
            self._engine.enterabs(
                event.ts, 0, self.execute_event, argument=(event.value, event.target))
        localtime: tuple = time.localtime()
        print(f"Scheduler: Starting the scheduling engine at {localtime[3]}:{localtime[4]}")
        self._engine.run()
        print("Scheduler: All events have been dispatched")

    def execute_event(self, value: str, target: str) -> None:
        current_time: int = int(self.scheduler_time())
        print(f"Scheduler: {current_time}, sending value {value} to target {target}...")
        if not self._debug:
            self._client.publish(target, payload=value, qos=1, retain=False)
        print("Scheduler: Sent")
        # Write to the logfile
        log_time: float = time.time()
        with open(self._cfg.log_path, "a") as f:
            log_entry: str = f"{log_time}\t{current_time}\t{target}\t{value}\n"
            f.write(log_entry)
        print("Scheduler: Log appended")
        Determine if we should add an event to the DB
        target_split: list = target.split("/")
        if target_split[0] == "scheduler":
            node_name = target_split[1]
            self.add_event(log_time, value, node_name)
            print("Scheduler: Added event to database")


if __name__ == "__main__":
    s = Scheduler("tests/files/test_trace.txt",
                  "files/scheduler_config.json")
    s.start()
