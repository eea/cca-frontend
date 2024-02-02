""" Convert html produced by blocks2html
"""

from bs4 import BeautifulSoup
from .blocks import text_to_blocks
# from uuid import uuid4


def convert_columns_block(fragment):
    __import__("pdb").set_trace()
    pass


converters = {"columnsBlock": convert_columns_block}


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

    blocks = text_to_blocks(fragment)
    assert len(blocks) == 1

    return blocks[0]


def deserialize_blocks(element):
    blocks = {}
    items = []

    for f in element.findChildren():
        blockuid = deserialize_block(f)
        if len(blockuid) != 2:
            continue  # converter not created yet
        uid, block = blockuid
        blocks[uid] = block
        items.append(uid)

    return {"blocks": blocks, "blocks_layout": {"items": items}}


def convert_html_to_content(text):
    tree = BeautifulSoup(text, "html.parser")
    fragments = tree.find("body").find_all("div", recursive=False)

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
