from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./sensot_trace.txt", "./sensor_config.json")
scheduler.start()
