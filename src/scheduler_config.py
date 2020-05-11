from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class SchedulerConfig:
    addr: str
    port: int
    name: str
    username: str
    password: str

    def __init__(self, addr: str, port: int, name: str, username: str, password: str) -> None:
        self.addr = addr
        self.port = port
        self.name = name
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(obj: Any) -> 'SchedulerConfig':
        assert isinstance(obj, dict)
        addr = from_str(obj.get("addr"))
        port = from_int(obj.get("port"))
        name = from_str(obj.get("name"))
        username = from_str(obj.get("username"))
        password = from_str(obj.get("password"))
        return SchedulerConfig(addr, port, name, username, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["addr"] = from_str(self.addr)
        result["port"] = from_int(self.port)
        result["name"] = from_str(self.name)
        result["username"] = from_str(self.username)
        result["password"] = from_str(self.password)
        return result


def scheduler_config_from_dict(s: Any) -> SchedulerConfig:
    return SchedulerConfig.from_dict(s)


def scheduler_config_to_dict(x: SchedulerConfig) -> Any:
    return to_class(SchedulerConfig, x)
