from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./simple_light_trace.txt", "./simple_light_config.json")
scheduler.start()
