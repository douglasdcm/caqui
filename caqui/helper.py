# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import base64
from caqui.cssify import cssify


def save_picture(session, path, file_name, response):
    with open(f"{path}/{file_name}-{session}.png", "wb") as f:
        f.write(base64.b64decode((response)))


def get_elements(response) -> list:
    values = response.get("value")
    return [list(value.values())[0] for value in values]


def get_element(response) -> str:
    value = response.get("value")
    # Google Chrome
    element = value.get("ELEMENT")
    if element:
        return element

    # Firefox
    return list(value.values())[0]


def convert_xpath_to_css_selector(locator_type: str, locator_value: str):
    try:
        if locator_type.lower() == "xpath":
            locator_value = cssify(locator_value)
            locator_type = "css selector"
    except Exception:
        # just ignore it and keep using the xpath selector
        pass
    return locator_type, locator_value
