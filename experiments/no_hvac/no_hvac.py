from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./no_hvac_trace.txt", "./no_hvac_config.json")
scheduler.start()
