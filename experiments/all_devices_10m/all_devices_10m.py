from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./all_devices_trace_10m.txt", "./all_devices_config_10m.json")
scheduler.start()
