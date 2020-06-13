from scheduler.main_scheduler import Scheduler

scheduler = Scheduler("./no_sensor_trace.txt", "./no_sensor_config.json")
scheduler.start()
