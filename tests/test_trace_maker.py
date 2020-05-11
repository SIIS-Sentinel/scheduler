from src.trace_maker import TraceMaker


def test_parse(tmp_path):
    assert TraceMaker("tests/files/test_schedule.json", tmp_path / "trace.txt")


def test_generate(tmp_path):
    trace = TraceMaker("tests/files/test_schedule.json", tmp_path / "trace.txt")
    trace.generate_trace()


def test_period(tmp_path):
    trace = TraceMaker("tests/files/test_period.json", tmp_path / "trace.txt", 0, 7)
    trace.generate_trace()
    nb_events = 7 * 24 * 60 / 2
    assert trace._trace.event_number <= nb_events


def test_write(tmp_path):
    trace = TraceMaker("tests/files/test_schedule.json", tmp_path / "trace.txt")
    trace.generate_trace()
    trace.write_trace()
