from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./all_devices_trace_2m.txt", "./all_devices_config_2m.json")
scheduler.start()
