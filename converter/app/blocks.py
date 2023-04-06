import json
import logging
from uuid import uuid4

from bs4 import BeautifulSoup

from .html2slate import text_to_slate

logger = logging.getLogger("app")


def make_tab_block(tabs):
    block_ids = [str(uuid4()) for _ in tabs]
    blocks = {}

    for i, tab in enumerate(tabs):
        blocks[block_ids[i]] = {
            "@type": "tab",
            "blocks": dict(tab['content']),
            "blocks_layout": {"items": [b[0] for b in tab['content']]}
        }

    data = {
        "@type": "tabs_block",
        "data": {
            "blocks": blocks,
            "blocks_layout": {
                "items": block_ids
            }
        }
    }
    return data


def block_tag(data, soup):
    element = soup.new_tag('block')
    element.string = json.dumps(data)

    return element


def convert_tabs(soup):
    nav_tabs = soup.find_all("ul", attrs={"class": "nav nav-tabs"})

    if not nav_tabs:
        return

    for ul in nav_tabs:
        div_content = ul.find_next_sibling("div", class_="tab-content")
        tab_structure = []
        tabs = ul.find_all('li')

        for li in tabs:
            tab_id = li.a.attrs['href'].replace('#', '')
            title = li.a.text

            tab_blocks = text_to_blocks(
                div_content.find_all(
                    "div", {"id": tab_id}, limit=1)[0]
            )
            logger.info("tabs %s", tab_blocks)

            tab_structure.append(
                {
                    "id": tab_id,
                    "title": title,
                    "content": tab_blocks
                })

        data = make_tab_block(tab_structure)
        div_content.decompose()
        ul.replace_with(block_tag(data, soup))


preprocessors = [
    convert_tabs
]


def text_to_blocks(text):
    if text and not isinstance(text, str):
        soup = text
    else:
        soup = BeautifulSoup(text, "html.parser")

    for proc in preprocessors:
        proc(soup)

    text = str(soup)

    slate = text_to_slate(text)

    return convert_slate_to_blocks(slate)


def convert_slate_to_blocks(slate):
    blocks = [[str(uuid4()), convert_block(block)] for block in slate]
    print('blocks', blocks)
    return blocks


def convert_block(block):
    # TODO: do the plaintext
    # TODO: detect replaced blocks

    return {"@type": "slate", "value": [block], "plaintext": ""}
