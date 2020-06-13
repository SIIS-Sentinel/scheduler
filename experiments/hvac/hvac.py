from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./hvac_trace.txt", "./hvac_config.json")
scheduler.start()
