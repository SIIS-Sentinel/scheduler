from src.full_trace import Trace


def test_order():
    trace = Trace()
    trace.add_event(0, "value", "target")
    trace.add_event(3, "value", "target")
    trace.add_event(1, "value", "target")
    trace.add_event(2, "value", "target")
    assert trace.event(0).ts == 0
    assert trace.event(1).ts == 1
    assert trace.event(2).ts == 2
    assert trace.event(3).ts == 3
