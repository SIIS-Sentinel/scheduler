from src.trace_maker import TraceMaker


def test_parse(tmp_path):
    assert TraceMaker("tests/files/schedule.json", tmp_path / "trace.txt")


def test_generate(tmp_path):
    trace = TraceMaker("tests/files/schedule.json", tmp_path / "trace.txt")
    trace.generate_trace()
