from .slate2html import slate_to_html


converters = {"slate": slate_to_html}


def convert_block_to_html(block_data):
    _type = block_data.get("@type", None)

    if _type is None:
        raise ValueError

    return converters[_type](block_data)


def convert_blocks_to_html(data):
    __import__("pdb").set_trace()
    order = data.blocks_layout["items"]
    blocks = data.blocks
    fragments = []

    for uid in order:
        block = blocks[uid]
        data = convert_block_to_html(block)
        fragments.append(data)

    return "\n".join(fragments)
