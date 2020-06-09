from hypothesis import given
from hypothesis.strategies import lists, integers
from typing import List

from scheduler.full_trace import Trace


@given(data=lists(integers()))
def test_order(data: List[int]):
    trace = Trace()
    for i in data:
        trace.add_event(i, "value", "target")
    assert trace.event_number == len(data)
    for i in range(trace.event_number - 1):
        assert trace.event(i).ts <= trace.event(i + 1).ts


def test_load():
    trace = Trace()
    trace.load_file("tests/files/basic_test_trace.txt")
    assert trace.event(0).ts == 1
    assert trace.event(1).ts == 2
    assert trace.event(2).ts == 3
    assert trace.event_number == 3


def test_load_blank_line():
    trace = Trace()
    trace.load_file('tests/files/blank_lines_trace.txt')
    assert trace.event(0).ts == 1
    assert trace.event(1).ts == 2
    assert trace.event(2).ts == 3
    assert trace.event_number == 3


def test_store(tmp_path):
    expected_content = "{'ts': 1, 'value': 'value_1', 'target': 'target_1'}\n\
{'ts': 2, 'value': 'value_2', 'target': 'target_2'}\n\
{'ts': 3, 'value': 'value_3', 'target': 'target_3'}"
    filename = tmp_path / "test_store.txt"
    trace = Trace()
    trace.add_event(2, "value_2", "target_2")
    trace.add_event(1, "value_1", "target_1")
    trace.add_event(3, "value_3", "target_3")
    trace.store_file(filename)
    assert filename.read_text() == expected_content
