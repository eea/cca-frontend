import json
from lxml.html import builder as E
from .slate2html import elements_to_text, slate_to_elements


TABLE_CELLS = {"header": E.TH, "data": E.TD}


def nop_converter(block_data):
    return None


def convert_slate(block_data):
    return slate_to_elements(block_data["value"])


def convert_slate_table(block_data):
    _type = block_data.pop("@type")
    data = block_data.pop("table")
    rows = data.pop("rows")
    attributes = {
        "data-block-type": _type,
        "data-volto-block": json.dumps(data),
    }
    children = []
    for row in rows:
        ecells = []
        for cell in row["cells"]:
            el = TABLE_CELLS[cell["type"]](*slate_to_elements(cell["value"]))
            ecells.append(el)

        erow = E.TR(*ecells)
        children.append(erow)

    etable = E.TABLE(*children)
    ediv = E.DIV(etable, **attributes)
    return [ediv]


def iterate_blocks(data):
    uids = data["blocks_layout"]["items"]
    blocks = data["blocks"]

    for uid in uids:
        yield (uid, blocks[uid])


def convert_columns_block(block_data):
    _type = block_data.pop("@type")
    data = block_data.pop("data")
    attributes = {
        "data-block-type": _type,
        "data-volto-block": json.dumps(block_data),
    }

    children = []
    for _, coldata in iterate_blocks(data):
        colelements = []
        for _, block in iterate_blocks(coldata):
            colelements.extend(convert_block_to_elements(block))
        column = E.DIV(*colelements)
        children.append(column)

    div = E.DIV(*children, **attributes)

    return [div]


def generic_block_converter(translate_fields):
    def converter(block_data):
        _type = block_data.pop("@type")

        fv = {}
        for name in translate_fields:
            value = block_data.pop(name, None)
            if value is not None:
                fv[name] = value

        attributes = {
            "data-block-type": _type,
            "data-volto-block": json.dumps(block_data),
        }

        children = [
            E.DIV(fv[name], **{"data-fieldname": name}) for name in translate_fields
        ]
        div = E.DIV(*children, **attributes)
        return [div]

    return converter


def convert_quote(block_data):
    value = block_data.pop("value")
    _type = block_data.pop("@type")
    attributes = {
        "data-block-type": _type,
        "data-volto-block": json.dumps(block_data),
    }
    children = slate_to_elements(value)
    div = E.DIV(*children, **attributes)
    return [div]


def convert_image(block_data):
    # print("img", block_data)
    attributes = {
        "src": block_data["url"],
        "data-volto-block": json.dumps(block_data),
    }
    return [E.IMG(**attributes)]


converters = {
    "slate": convert_slate,
    "slateTable": convert_slate_table,
    "title": nop_converter,
    "quote": convert_quote,
    "image": convert_image,
    "columnsBlock": convert_columns_block,
    "nextCloudVideo": generic_block_converter(["title"]),
}


def convert_block_to_elements(block_data):
    _type = block_data.get("@type", None)

    if _type is None:
        raise ValueError

    if _type not in converters:
        print(f"{_type} has no block handler")
        return ""

    return converters[_type](block_data)


def convert_blocks_to_html(data):
    order = data.blocks_layout["items"]
    blocks = data.blocks
    fragments = []
    __import__("pdb").set_trace()

    for uid in order:
        block = blocks[uid]
        elements = convert_block_to_elements(block)
        if elements:
            html = elements_to_text(elements)
            fragments.append(html)

    return "\n".join(fragments)
