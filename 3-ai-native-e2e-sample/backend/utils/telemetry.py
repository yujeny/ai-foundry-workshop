import os
import contextlib
from enum import Enum

class StatusCode(Enum):
    ERROR = "ERROR"
    OK = "OK"

class Status:
    def __init__(self, status_code: StatusCode):
        self.status_code = status_code

class NoopSpan:
    def __init__(self, name: str = None):
        self.name = name

    def set_attribute(self, key: str, value: any) -> None:
        pass

    def record_exception(self, exception: Exception) -> None:
        pass

    def set_status(self, status: any) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Tracer:
    def start_as_current_span(self, name: str):
        return NoopSpan(name)

tracer = Tracer() 