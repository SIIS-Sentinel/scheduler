from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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
    log_path: str
    overwrite_log: bool
    cafile: str
    certfile: str
    keyfile: str
    db_path: str

    def __init__(self, addr: str, port: int, name: str, username: str, password: str, log_path: str, overwrite_log: bool, cafile: str, certfile: str, keyfile: str, db_path: str) -> None:
        self.addr = addr
        self.port = port
        self.name = name
        self.username = username
        self.password = password
        self.log_path = log_path
        self.overwrite_log = overwrite_log
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        self.db_path = db_path

    @staticmethod
    def from_dict(obj: Any) -> 'SchedulerConfig':
        assert isinstance(obj, dict)
        addr = from_str(obj.get("addr"))
        port = from_int(obj.get("port"))
        name = from_str(obj.get("name"))
        username = from_str(obj.get("username"))
        password = from_str(obj.get("password"))
        log_path = from_str(obj.get("log_path"))
        overwrite_log = from_bool(obj.get("overwrite_log"))
        cafile = from_str(obj.get("cafile"))
        certfile = from_str(obj.get("certfile"))
        keyfile = from_str(obj.get("keyfile"))
        db_path = from_str(obj.get("db_path"))
        return SchedulerConfig(addr, port, name, username, password, log_path, overwrite_log, cafile, certfile, keyfile, db_path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["addr"] = from_str(self.addr)
        result["port"] = from_int(self.port)
        result["name"] = from_str(self.name)
        result["username"] = from_str(self.username)
        result["password"] = from_str(self.password)
        result["log_path"] = from_str(self.log_path)
        result["overwrite_log"] = from_bool(self.overwrite_log)
        result["cafile"] = from_str(self.cafile)
        result["certfile"] = from_str(self.certfile)
        result["keyfile"] = from_str(self.keyfile)
        result["db_path"] = from_str(self.db_path)
        return result


def scheduler_config_from_dict(s: Any) -> SchedulerConfig:
    return SchedulerConfig.from_dict(s)


def scheduler_config_to_dict(x: SchedulerConfig) -> Any:
    return to_class(SchedulerConfig, x)
