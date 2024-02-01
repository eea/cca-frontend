from lxml.html import builder as E
from .slate2html import slate_to_html, elements_to_text, slate_to_elements


def convert_slate(block_data):
    value = slate_to_html(block_data["value"])
    return value


def nop_converter(*args):
    return


def convert_quote(block_data):
    attributes = {"data-block_type": "quote"}
    children = slate_to_elements(block_data["value"])
    div = E.DIV(*children, **attributes)
    return elements_to_text([div])


converters = {"slate": convert_slate,
              "title": nop_converter, "quote": convert_quote}


def convert_block_to_html(block_data):
    _type = block_data.get("@type", None)

    if _type is None:
        raise ValueError

    if _type not in converters:
        print(f"{_type} has no block handler")
        return ""

    return converters[_type](block_data)


def convert_blocks_to_html(data):
    # __import__("pdb").set_trace()
    order = data.blocks_layout["items"]
    blocks = data.blocks
    fragments = []

    for uid in order:
        block = blocks[uid]
        data = convert_block_to_html(block)
        if data:
            fragments.append(data)

    return "\n".join(fragments)
