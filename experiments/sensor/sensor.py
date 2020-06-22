from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./sensor_trace.txt", "./sensor_config.json")
scheduler.start()
