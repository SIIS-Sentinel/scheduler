from src.trace_maker import TraceMaker
from src.full_trace import Trace

import filecmp


def test_all(tmp_path):
    maker = TraceMaker("tests/files/test_schedule.json", tmp_path / "trace.txt")
    maker.generate_trace()
    maker.write_trace()
    trace = Trace()
    trace.load_file(tmp_path / "trace.txt")
    trace.store_file(tmp_path / "trace_loaded.txt")
    assert filecmp.cmp(tmp_path / "trace.txt", tmp_path / "trace_loaded.txt")
