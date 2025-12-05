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
    "(?P<matched>(?P<mattr>@?%(attribute)s=[\"'](?P<mvalue>%(value)s))[\"']"  # noqa: E501 # [@id="bleh"] and [text()="meh"]
    "|"
    "(?P<contained>contains\\((?P<cattr>@?%(attribute)s,\\s*[\"'](?P<cvalue>%(value)s)[\"']\\))"  # noqa: E501 # [contains(text(), "bleh")] or [contains(@id, "bleh")]
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

    css: list = []
    position: int = 0

    while position < len(xpath):
        node = prog.match(xpath[position:])
        if node is None:
            raise XpathException(f"Invalid or unsupported Xpath: {xpath}")
        match = node.groupdict()

        parts = []

        if position != 0:
            parts.append(" " if match["nav"] == "//" else " > ")

        if match["tag"] != "*":
            parts.append(match["tag"] or "")

        if match["idvalue"]:
            parts.append(f"#{match['idvalue'].replace(' ', '#')}")
        elif match["matched"]:
            mattr = match["mattr"]
            mvalue = match["mvalue"]
            if mattr == "@id":
                parts.append(f"#{mvalue.replace(' ', '#')}")
            elif mattr == "@class":
                parts.append(f".{mvalue.replace(' ', '.')}")
            elif mattr in ("text()", "."):
                parts.append(f":contains(^{mvalue}$)")
            elif mattr:
                if " " in mvalue:
                    mvalue = f'"{mvalue}"'
                parts.append(f"[{mattr.replace('@', '')}={mvalue}]")
        elif match["contained"]:
            cattr = match["cattr"]
            cvalue = match["cvalue"]
            if cattr.startswith("@"):
                parts.append(f"[{cattr.replace('@', '')}*={cvalue}]")
            elif cattr == "text()":
                parts.append(f":contains({cvalue})")

        if match["nth"]:
            parts.append(f":nth-of-type({match['nth']})")

        css.append("".join(parts))
        position += node.end()

    return "".join(css).strip()
