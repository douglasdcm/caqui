# Copyright (c) 2025 Santiycr
#
# This file is part of Santiycr/cssify.
# Visit: https://github.com/santiycr/cssify
#
# Copyright (C) 2025 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import re

sub_regexes = {
    "tag": r"([a-zA-Z][a-zA-Z0-9]{0,10}|\*)",
    "attribute": r"[.a-zA-Z_:][-\w:.]*(\(\))?)",
    "value": r"\s*[\w/:][-/\w\s,:;.]*",
}

validation_re = (
    "(?P<node>"
    "("
    "^id\\([\"']?(?P<idvalue>%(value)s)[\"']?\\)"  # special case! id(idValue)
    "|"
    "(?P<nav>//?)(?P<tag>%(tag)s)"  # //div
    r"(\[("
    "(?P<matched>(?P<mattr>@?%(attribute)s=[\"'](?P<mvalue>%(value)s))[\"']"  # [@id="bleh"] and [text()="meh"]
    "|"
    "(?P<contained>contains\\((?P<cattr>@?%(attribute)s,\\s*[\"'](?P<cvalue>%(value)s)[\"']\\))"  # [contains(text(), "bleh")] or [contains(@id, "bleh")]
    r")\])?"
    r"(\[(?P<nth>\d+)\])?"
    ")"
    ")" % sub_regexes
)

prog = re.compile(validation_re)


class XpathException(Exception):
    pass


def cssify(xpath: str):
    """
    Get your XPATHs translated to css automatically! (don't go to crazy on what
    you want to translate, this script is smart but won't do your breakfast).
    """

    css: str = ""
    position: int = 0

    while position < len(xpath):
        node = prog.match(xpath[position:])
        if node is None:
            raise XpathException(f"Invalid or unsupported Xpath: {xpath}")
        match = node.groupdict()

        nav: str = ""
        if position != 0:
            nav = " " if match["nav"] == "//" else " > "

        tag: str = "" if match["tag"] == "*" else match["tag"] or ""

        attr: str = ""
        if match["idvalue"]:
            attr = f"#{match['idvalue'].replace(' ', '#')}"
        elif match["matched"]:
            if match["mattr"] == "@id":
                attr = f"#{match['mvalue'].replace(' ', '#')}"
            elif match["mattr"] == "@class":
                attr = f".{match['mvalue'].replace(' ', '.')}"
            elif match["mattr"] in ["text()", "."]:
                attr = f":contains(^{match['mvalue']}$)"
            elif match["mattr"]:
                if match["mvalue"].find(" ") != -1:
                    mvalue: str = match["mvalue"]
                    match["mvalue"] = f'"{mvalue}"'
                attr = f"[{match['mattr'].replace('@', '')}={match['mvalue']}]"
        elif match["contained"]:
            if match["cattr"].startswith("@"):
                attr = f"[{match['cattr'].replace('@', '')}*={match['cvalue']}]"
            elif match["cattr"] == "text()":
                attr = f":contains({match['cvalue']})"

        nth: str = ""
        if match["nth"]:
            nth = f":nth-of-type({match['nth']})"

        node_css: str = nav + tag + attr + nth

        css += node_css
        position += node.end()
    else:
        css = css.strip()
        return css
