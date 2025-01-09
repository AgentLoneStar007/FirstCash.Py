from .version import Version
from .http_content import HTTPContent
from .http_method import HTTPMethod


class HTTPRequestMessage:
    version: Version
    content: HTTPContent
    method: HTTPMethod
    request_uri: str
    headers: list[object]
    properties: dict
