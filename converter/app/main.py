from dataclasses import dataclass

from starlite import LoggingConfig, Starlite, get, post

from .blocks import text_to_blocks
from .html2slate import text_to_slate


@dataclass
class HTML:
    html: str


@get(path="/healthcheck")
def health_check() -> str:
    return "healthy"


@post(path="/html")
def html(data: HTML) -> str:
    html = data.html
    return {"data": text_to_slate(html)}


@post(path="/toblocks")
def toblocks(data: HTML) -> str:
    html = data.html
    return {"data": text_to_blocks(html)}


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
