import json
import logging
from dataclasses import dataclass
from typing import Any, Dict

from litestar import Litestar, get, post, Request
from litestar.status_codes import HTTP_200_OK

from .blocks import text_to_blocks
from .html2slate import text_to_slate
from .blocks2html import convert_blocks_to_html
from .tests import run

logger = logging.getLogger()


@dataclass
class HTML:
    html: str


@dataclass
class Blocks:
    blocks: Any
    blocks_layout: Any


@dataclass
class Response:
    data: Any


@get(path="/healthcheck")
async def health_check() -> str:
    return "healthy"


@get(path="/test")
async def run_tests() -> str:
    run()
    return "healthy"


@post(path="/html")
async def html(data: HTML) -> str:
    html = data.html
    return {"data": text_to_slate(html)}


@post(path="/toblocks", status_code=HTTP_200_OK)
async def toblocks(data: HTML) -> Dict:
    html = data.html
    data = text_to_blocks(html)

    logger.info("Blocks: \n%s", json.dumps(data, indent=2))
    return {"data": data}


@post(path="/blocks2html", status_code=HTTP_200_OK)
async def handle_block2html(data: Blocks, request: Request) -> Dict:
    # j = await request.json()
    # __import__("pdb").set_trace()
    html = convert_blocks_to_html(data)

    logger.info("HTML: \n%s", html)
    return {"html": html}


app = Litestar(
    route_handlers=[health_check, html, toblocks, handle_block2html],
    debug=True,
)
