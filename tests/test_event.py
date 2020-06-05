from hypothesis import given
from hypothesis.strategies import text, integers, floats

from scheduler.event import Event


def test_explicit():
    ts = 2
    value = "bad"
    target = "this"
    event = Event(ts, value, target)
    assert event._ts == ts
    assert event._value == value
    assert event._target == target


def test_deserial():
    buffer = "{'ts': 3, 'value': 'good', 'target': 'there'}"
    event = Event(buffer=buffer)
    assert event._ts == 3
    assert event._target == "there"
    assert event._value == "good"


@given(ts=integers(), val=text(), tar=text())
def test_serial(ts: int, val: str, tar: str):
    event = Event(ts, val, tar)
    serial = repr(event)
    data: dict = {
        'ts': ts,
        'value': val,
        'target': tar
    }
    assert serial == repr(data)
