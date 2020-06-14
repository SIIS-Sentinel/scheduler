from scheduler.main_scheduler import Scheduler

trace_path = "tests/files/test_trace.txt"
config_path = "tests/files/test_load_config.json"


def test_load_config():
    sched = Scheduler(
        trace_path,
        config_path,
        debug=True,
        db_path="postgresql://pi:password@192.168.0.110/sentinel"
    )
    assert sched._cfg.addr == "test_addr"
    assert sched._cfg.username == "test_user"
    assert sched._cfg.password == "test_password"
    assert sched._cfg.name == "test_name"
    assert sched._cfg.port == 12345
    assert sched._cfg.log_path == "test.log"
    assert sched._cfg.overwrite_log is True
    assert sched._cfg.cafile == "test_ca.pem"
    assert sched._cfg.certfile == "test_cert.crt"
    assert sched._cfg.keyfile == "test_key.key"


def test_empty_trace(tmp_path):
    path = tmp_path / "empty_trace.txt"
    with open(path, "w") as f:
        f.write("")
    sched = Scheduler(
        path,
        config_path,
        debug=True,
        db_path="postgresql://pi:password@hub.local/sentinel"
    )
    sched.start()


def test_run(monkeypatch):

    def mock_time(obj):
        return 1e8

    def mock_sleep(obj, delay):
        return

    monkeypatch.setattr(Scheduler, "scheduler_time", mock_time)
    monkeypatch.setattr(Scheduler, "scheduler_sleep", mock_sleep)
    sched = Scheduler(
        trace_path,
        config_path,
        debug=True,
        db_path="postgresql://pi:password@hub.local/sentinel"
    )
    sched.start()
