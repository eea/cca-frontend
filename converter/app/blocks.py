import json
import logging
from uuid import uuid4

from bs4 import BeautifulSoup

from .html2slate import text_to_slate

logger = logging.getLogger()


def make_tab_block(tabs):
    block_ids = [str(uuid4()) for _ in tabs]
    blocks = {}

    for i, tab in enumerate(tabs):
        blocks[block_ids[i]] = {
            "@type": "tab",
            "title": tab['title'],
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


def make_accordion_block(panels):
    block_ids = [str(uuid4()) for _ in panels]

    blocks = {}

    for i, panel in enumerate(panels):
        blocks[block_ids[i]] = {
            "@type": "accordionPanel",
            "title": panel['title'],
            "blocks": dict(panel['content']),
            "blocks_layout": {"items": [b[0] for b in panel['content']]}
        }

    data = {
        "@type": "accordion",
        "collapsed": "true",
        "non_exclusive": "true",
        "right_arrows": "true",
        "styles": {},
        "data": {
            "blocks": blocks,
            "blocks_layout": {
                "items": block_ids
            }
        }
    }
    return data


_tag = None


def block_tag(data, soup_or_tag):
    if soup_or_tag.parent:
        soup = list(soup_or_tag.parents)[-1]
    else:
        soup = soup_or_tag

    element = soup.new_tag('voltoblock')
    element['data-voltoblock'] = json.dumps(data)

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
            if li.a is None:
                # broken html generated
                continue

            tab_id = li.a.attrs['href'].replace('#', '')
            title = li.a.text

            tab_blocks = text_to_blocks(
                div_content.find_all(
                    "div", {"id": tab_id}, limit=1)[0]
            )

            tab_structure.append(
                {
                    "id": tab_id,
                    "title": title,
                    "content": tab_blocks
                })

        data = make_tab_block(tab_structure)
        ul.replace_with(block_tag(data, soup))  # no need to decompose
        div_content.decompose()


def convert_iframe(soup):
    # TODO: also apply the height
    iframes = soup.find_all("iframe")

    for tag in iframes:
        data = {"@type": "maps", "url": tag.attrs['src']}
        tag.replace_with(block_tag(data, soup))


def convert_button(soup):
    buttons = soup.find_all("a", attrs={"class": "bluebutton"})

    for button in buttons:
        target = button.attrs['target'] if button.has_attr(
            'target') else "_self"

        data = {
            "@type": "callToActionBlock",
            "text": button.text,
            "href": button.attrs['href'],
            "target": target,
            "styles": {
                "icon": "ri-share-line",
                "theme": "primary",
                "align": "left"
            },
        }

        parent = button.find_parent("p")
        if parent:
            parent.replace_with(block_tag(data, soup))
        else:
            button.replace_with(block_tag(data, soup))


def convert_accordion(soup):
    accordions = soup.find_all("div", attrs={"class": "panel-group"})

    if not accordions:
        return

    for div in accordions:
        panels = div.find_all("div", attrs={"class": "panel"})

        panels_structure = []
        for panel in panels:
            panel_id = panel.find_all(
                "div", attrs={"class": "panel-heading"})[0].attrs['id'].split(
                "-heading")[0]
            panel_title = panel.find_all(
                "h4", attrs={"class": "panel-title"})[0].text

            panel_body = panel.find_all(
                "div", attrs={"class": "panel-body"})[0]

            panels_structure.append(
                {
                    "id": panel_id,
                    "title": panel_title,
                    "content": text_to_blocks(panel_body)
                }

            )

        data = make_accordion_block(panels_structure)
        div.replace_with(block_tag(data, soup))


preprocessors = [
    convert_tabs,
    convert_iframe,
    convert_accordion,
    convert_button,
]


def text_to_blocks(text_or_element):
    if text_or_element and not isinstance(text_or_element, str):
        soup = text_or_element
    else:
        soup = BeautifulSoup(text_or_element, "html.parser")

    for proc in preprocessors:
        proc(soup)

    new_text = str(soup)

    slate = text_to_slate(new_text)

    blocks = convert_slate_to_blocks(slate)
    return blocks


def convert_slate_to_blocks(slate):
    blocks = [[str(uuid4()), convert_block(paragraph)] for paragraph in slate]
    return blocks


def convert_block(block):
    # TODO: do the plaintext

    if block.get('type') == 'voltoblock':
        return block['data']

    return {"@type": "slate", "value": [block], "plaintext": ""}
