from __future__ import annotations

from collections.abc import Callable

from tempestwx._http import Request, Response
from tempestwx._http.client import send_and_process as _send_and_process

from .error_handler import handle_errors


def make_request(post_func: Callable) -> Callable:
    """
    Decorate an endpoint to make an HTTP request and process the response.

    Parameters
    ----------
    post_func
        function to call with response JSON content
    """

    def parse_response(request: Request, response: Response):
        handle_errors(request, response)
        return post_func(response.content)

    return _send_and_process(parse_response)
