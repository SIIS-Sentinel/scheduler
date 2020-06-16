from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./debug_trace.txt", "./debug_config.json")
scheduler.start()
