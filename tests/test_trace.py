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


def test_load():
    trace = Trace()
    trace.load_file("tests/files/test_load.txt")
    assert trace.event(0).ts == 1
    assert trace.event(1).ts == 2
    assert trace.event(2).ts == 3


def test_store(tmp_path):
    expected_content = "{'ts': 1, 'value': 'value_1', 'target': 'target_1'}\n\
{'ts': 2, 'value': 'value_2', 'target': 'target_2'}\n\
{'ts': 3, 'value': 'value_3', 'target': 'target_3'}"
    filename = tmp_path / "test_store.txt"
    trace = Trace()
    trace.add_event(1, "value_1", "target_1")
    trace.add_event(2, "value_2", "target_2")
    trace.add_event(3, "value_3", "target_3")
    trace.store_file(filename)
    assert filename.read_text() == expected_content
