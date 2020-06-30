from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./all_devices_trace_1m.txt", "./all_devices_config_1m.json")
scheduler.start()
