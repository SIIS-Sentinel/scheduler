from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./all_devices_trace.txt", "./all_devices_config.json")
scheduler.start()
