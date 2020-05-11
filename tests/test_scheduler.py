from src.scheduler import Scheduler

trace_path = "tests/files/test_trace.txt"
config_path = "tests/files/test_load_config.json"


def test_load_config():
    sched = Scheduler(trace_path, config_path, True)
    assert sched._cfg.addr == "test_addr"
    assert sched._cfg.username == "test_user"
    assert sched._cfg.password == "test_password"
    assert sched._cfg.name == "test_name"
    assert sched._cfg.port == 12345


def test_empty_trace(tmp_path):
    path = tmp_path / "empty_trace.txt"
    with open(path, "w") as f:
        f.write("")
    sched = Scheduler(path, config_path, True)
    sched.start()


def test_run(monkeypatch):

    def mock_time(obj):
        return 1e8

    def mock_sleep(obj, delay):
        return

    monkeypatch.setattr(Scheduler, "scheduler_time", mock_time)
    monkeypatch.setattr(Scheduler, "scheduler_sleep", mock_sleep)
    sched = Scheduler(trace_path, config_path, True)
    sched.start()
