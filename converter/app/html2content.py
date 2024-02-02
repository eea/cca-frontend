""" Convert html produced by blocks2html
"""

import json
from bs4 import BeautifulSoup

from .html2slate import HTML2Slate
from .blocks import text_to_blocks
from uuid import uuid4


def get_elements(node):
    for child in node.children:
        if child.name:
            yield child


def convert_columns_block(fragment):
    rawdata = fragment.attrs["data-volto-block"]

    data = json.loads(rawdata)
    data["@type"] = "columnsBlock"

    colblockdata = {"blocks_layout": {"items": []}, "blocks": {}}

    for column in get_elements(fragment):
        coldata = deserialize_blocks(column)
        coluid = str(uuid4())
        colblockdata["blocks"][coluid] = coldata
        colblockdata["blocks_layout"]["items"].append(coluid)

    data["data"] = colblockdata
    uid = str(uuid4())

    return [uid, data]


def convert_quote_block(fragment):
    rawdata = fragment.attrs["data-volto-block"]

    data = json.loads(rawdata)
    data["@type"] = "quote"
    elements = list(get_elements(fragment))
    data["value"] = HTML2Slate().from_elements(elements)

    uid = str(uuid4())

    return [uid, data]


converters = {"columnsBlock": convert_columns_block,
              "quote": convert_quote_block}


def deserialize_block(fragment):
    """Convert a lxml fragment to a Volto block. This assumes that the HTML
    structure has been previously exported with block2html"""
    _type = fragment.attrs.get("data-block-type")
    if _type:
        if _type not in converters:
            print(f"Block deserializer needed: {_type}")
            return []
        else:
            deserializer = converters[_type]
            return deserializer(fragment)

    # fallback to slate deserializer
    blocks = text_to_blocks(fragment)
    assert len(blocks) == 1

    return blocks[0]


def deserialize_blocks(element):
    blocks = {}
    items = []

    for f in get_elements(element):
        blockuid = deserialize_block(f)
        if len(blockuid) != 2:
            continue  # converter not created yet
        uid, block = blockuid
        blocks[uid] = block
        items.append(uid)

    return {"blocks": blocks, "blocks_layout": {"items": items}}


def convert_html_to_content(text: str):
    tree = BeautifulSoup(text, "html.parser")
    body = tree.find("body")
    fragments = body.find_all("div", recursive=False)

    data = {}

    for f in fragments:
        if not hasattr(f, "attrs"):
            continue
        field = f.attrs.get("data-field")
        if not field:
            continue

        if field == "blocks":
            data[field] = deserialize_blocks(f)
        else:
            data[field] = f.text or ""

    return data
