# (currently unused)

from .version import Version
from .http_content import HTTPContent
from .http_status_code import HTTPStatusCode


class HTTPResponseMessage:
    version: Version
    content: HTTPContent
    status_code: HTTPStatusCode
    reason_phrase: str
    headers: list[object]  # seriously? object is our data type?
    request_message: None
    is_success_status_code: bool
