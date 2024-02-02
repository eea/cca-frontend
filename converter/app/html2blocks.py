from bs4 import BeautifulSoup
from uuid import uuid4


def fragments_fromstring(text):
    tree = BeautifulSoup(text, "html.parser")
    return list(tree)


def deserialize_block(fragment):
    pass


def convert_html_to_blocks(text):
    fragments = fragments_fromstring(text)

    blocks = {}
    items = []

    for f in fragments:
        block = deserialize_block(f)
        uid = str(uuid4())
        blocks[uid] = block
        items.append(uid)

    return {"blocks": blocks, "blocks_layout": {"items": items}}
