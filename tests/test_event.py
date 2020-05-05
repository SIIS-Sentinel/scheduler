from src.event import Event


def test_explicit():
    ts = 2.17
    value = "bad"
    target = "this"
    event = Event(ts, value, target)
    assert event._ts == ts
    assert event._value == value
    assert event._target == target


def test_deserial():
    buffer = "{'ts': 3.14, 'value': 'good', 'target': 'there'}"
    event = Event(buffer=buffer)
    assert event._ts == 3.14
    assert event._target == "there"
    assert event._value == "good"


def test_serial():
    event = Event(10.2, "val", "tar")
    serial = repr(event)
    assert serial == "{'ts': 10.2, 'value': 'val', 'target': 'tar'}"
