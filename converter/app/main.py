from dataclasses import dataclass
from typing import Any, Dict

from starlite import LoggingConfig, Starlite, get, post
from starlite.status_codes import HTTP_200_OK

from .blocks import text_to_blocks
from .html2slate import text_to_slate


@dataclass
class HTML:
    html: str


@dataclass
class Response:
    data: Any


@get(path="/healthcheck")
def health_check() -> str:
    return "healthy"


@post(path="/html")
def html(data: HTML) -> str:
    html = data.html
    return {"data": text_to_slate(html)}


@post(path="/toblocks", status_code=HTTP_200_OK)
def toblocks(data: HTML) -> Dict:
    html = data.html
    data = text_to_blocks(html)
    return {"data": data}


logging_config = LoggingConfig(
    loggers={
        "app": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)

app = Starlite(
    route_handlers=[health_check, html, toblocks],
    logging_config=logging_config,
    debug=True,
)
