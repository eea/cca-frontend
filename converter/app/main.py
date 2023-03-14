from dataclasses import dataclass

from starlite import Starlite, get, post
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


app = Starlite(
    route_handlers=[health_check, html],
)
