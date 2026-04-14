from typing import Protocol, IO


"Protocol for file upload, e.g. for hotel images"


class UploadFileProtocol(Protocol):
    filename: str
    file: IO[bytes]


"""Login response protocol, e.g. for login method of auth service"""


class LoginResponseProtocol(Protocol):
    def set_cookie(self, key: str, value: str = "") -> None: ...


"""Logout response protocol, e.g. for logout method of auth service"""


class LogoutResponseProtocol(Protocol):
    def delete_cookie(self, key: str) -> None: ...
