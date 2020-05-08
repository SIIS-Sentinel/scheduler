from typing import List, Optional, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Condition:
    days: List[int]
    time_start: Optional[str]
    time_end: Optional[str]

    def __init__(self, days: List[int], time_start: Optional[str], time_end: Optional[str]) -> None:
        self.days = days
        self.time_start = time_start
        self.time_end = time_end

    @staticmethod
    def from_dict(obj: Any) -> 'Condition':
        assert isinstance(obj, dict)
        days = from_list(from_int, obj.get("days"))
        time_start = from_union([from_str, from_none], obj.get("time_start"))
        time_end = from_union([from_str, from_none], obj.get("time_end"))
        return Condition(days, time_start, time_end)

    def to_dict(self) -> dict:
        result: dict = {}
        result["days"] = from_list(from_int, self.days)
        result["time_start"] = from_union([from_str, from_none], self.time_start)
        result["time_end"] = from_union([from_str, from_none], self.time_end)
        return result


class State:
    name: Optional[str]
    min_duration: Optional[int]
    max_duration: Optional[int]
    event: Optional[str]
    time: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]

    def __init__(self, name: Optional[str], min_duration: Optional[int], max_duration: Optional[int], event: Optional[str], time: Optional[str], min_value: Optional[int], max_value: Optional[int]) -> None:
        self.name = name
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.event = event
        self.time = time
        self.min_value = min_value
        self.max_value = max_value

    @staticmethod
    def from_dict(obj: Any) -> 'State':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        min_duration = from_union([from_int, from_none], obj.get("min_duration"))
        max_duration = from_union([from_int, from_none], obj.get("max_duration"))
        event = from_union([from_str, from_none], obj.get("event"))
        time = from_union([from_str, from_none], obj.get("time"))
        min_value = from_union([from_int, from_none], obj.get("min_value"))
        max_value = from_union([from_int, from_none], obj.get("max_value"))
        return State(name, min_duration, max_duration, event, time, min_value, max_value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["min_duration"] = from_union([from_int, from_none], self.min_duration)
        result["max_duration"] = from_union([from_int, from_none], self.max_duration)
        result["event"] = from_union([from_str, from_none], self.event)
        result["time"] = from_union([from_str, from_none], self.time)
        result["min_value"] = from_union([from_int, from_none], self.min_value)
        result["max_value"] = from_union([from_int, from_none], self.max_value)
        return result


class ScheduleElement:
    name: str
    elem_type: str
    condition: Condition
    event: Optional[str]
    target: str
    states: Optional[List[State]]
    update_period: Optional[int]

    def __init__(self, name: str, elem_type: str, condition: Condition, event: Optional[str], target: str, states: Optional[List[State]], update_period: Optional[int]) -> None:
        self.name = name
        self.elem_type = elem_type
        self.condition = condition
        self.event = event
        self.target = target
        self.states = states
        self.update_period = update_period

    @staticmethod
    def from_dict(obj: Any) -> 'ScheduleElement':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        elem_type = from_str(obj.get("elem_type"))
        condition = Condition.from_dict(obj.get("condition"))
        event = from_union([from_str, from_none], obj.get("event"))
        target = from_str(obj.get("target"))
        states = from_union([lambda x: from_list(State.from_dict, x), from_none], obj.get("states"))
        update_period = from_union([from_int, from_none], obj.get("update_period"))
        return ScheduleElement(name, elem_type, condition, event, target, states, update_period)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["elem_type"] = from_str(self.elem_type)
        result["condition"] = to_class(Condition, self.condition)
        result["event"] = from_union([from_str, from_none], self.event)
        result["target"] = from_str(self.target)
        result["states"] = from_union([lambda x: from_list(lambda x: to_class(State, x), x), from_none], self.states)
        result["update_period"] = from_union([from_int, from_none], self.update_period)
        return result


def schedule_from_dict(s: Any) -> List[ScheduleElement]:
    return from_list(ScheduleElement.from_dict, s)


def schedule_to_dict(x: List[ScheduleElement]) -> Any:
    return from_list(lambda x: to_class(ScheduleElement, x), x)
