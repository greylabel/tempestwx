from httpx import codes

from tempestwx._http import Request, Response
from tempestwx._http.error import get_error

error_format = "Error in {url}: {code}: {msg}"


def parse_error_message(response: Response) -> str:
    """Extract error status message from response content."""
    status = getattr(response, "status", "")
    if response.content is None:
        return status
    error = response.content["status"]
    message = error.get("status_message", status)
    return message


def handle_errors(request: Request, response: Response) -> None:
    """Parse response and raise errors."""
    if codes.is_error(response.status_code):
        error_str = error_format.format(
            url=response.url,
            code=response.status_code,
            msg=parse_error_message(response),
        )
        error_cls = get_error(response.status_code)
        raise error_cls(error_str, request=request, response=response)
