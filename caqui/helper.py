# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import base64
from functools import lru_cache

from caqui.by import By
from caqui.constants import ELEMENT_JSONWIRE, ELEMENT_W3C
from caqui.cssify import cssify


def save_picture(session: str, path: str, file_name: str, response: str) -> None:
    """
    Save a screenshot to a file.
    :param session: session id
    :param path: path to save the file
    :param file_name: name of the file
    :param response: base64 encoded screenshot
    """
    with open(f"{path}/{file_name}-{session}.png", "wb") as f:
        f.write(base64.b64decode((response)))


def get_elements(response: dict) -> list:
    """
    Extract the first value from each item in the 'value' key of a response dictionary.

    Args:
        response (dict): A dictionary containing a 'value' key with a list of dictionaries.

    Returns:
        list: A list containing the first value from each dictionary in the 'value' list.

    Example:
        >>> response = {"value": [{"key1": "val1", "key2": "val2"}, {"key3": "val3"}]}
        >>> get_elements(response)
        ['val1', 'val3']
    """
    values = response.get("value", {})
    return [list(value.values())[0] for value in values]


def get_element(response: dict) -> str:
    """Extract the element identifier from a WebDriver response payload.

    The function expects `response` to be a mapping containing a "value" mapping.
    For Chrome-based WebDriver responses the element id is usually stored under
    the ELEMENT key. For Firefox/Gecko the element id is commonly provided as
    the first value of the inner mapping.

    Args:
        response (dict): A WebDriver response dict with a "value" mapping that
                         contains either the ELEMENT key (Chrome) or another
                         single key whose value is the element id (Firefox).

    Returns:
        str: The extracted element identifier.

    Raises:
        AttributeError: If `response` does not contain a "value" mapping (i.e. when
                        `response.get("value")` returns None), attribute access
                        on `None` will raise.
    """
    value = response.get("value", {})
    # Google Chrome
    element = value.get(ELEMENT_W3C)
    if element:
        return element

    # Firefox
    return list(value.values())[0]


def get_element_jsonwire(response: dict) -> str:
    """Extract the element identifier from a WebDriver response payload.

    The function expects `response` to be a mapping containing a "value" mapping.
    For Chrome-based WebDriver responses the element id is usually stored under
    the ELEMENT key. For Firefox/Gecko the element id is commonly provided as
    the first value of the inner mapping.

    Args:
        response (dict): A WebDriver response dict with a "value" mapping that
                         contains either the ELEMENT key (Chrome) or another
                         single key whose value is the element id (Firefox).

    Returns:
        str: The extracted element identifier.

    Raises:
        AttributeError: If `response` does not contain a "value" mapping (i.e. when
                        `response.get("value")` returns None), attribute access
                        on `None` will raise.
    """
    value = response.get("value", {})
    # Google Chrome
    element = value.get(ELEMENT_JSONWIRE)
    if element:
        return element

    # Firefox
    return list(value.values())[0]


@lru_cache(maxsize=42)
def convert_locator_to_css_selector(locator_type: str, locator_value: str) -> tuple:
    """
    Convert an XPath and Nane locator to a CSS selector if possible.

    This function attempts to convert an locator expression to an equivalent
    CSS selector. If the conversion fails, the original locator type and value are
    returned unchanged. Results are cached for performance optimization.

    Args:
        locator_type (str): The type of locator (e.g., "xpath", "name").
        locator_value (str): The locator expression value to convert.

    Returns:
        tuple: A tuple containing (locator_type, locator_value) where locator_type
            is either "css selector" if conversion succeeded, or the original
            locator_type if conversion failed or was not applicable.

    Note:
        This function uses LRU caching with a maximum size of 32 entries to
        optimize repeated conversions of the same locator values.
    """
    if locator_type.lower() == By.ID:
        locator_value = f"#{locator_value}"
        locator_type = By.CSS_SELECTOR
        return locator_type, locator_value

    if locator_type.lower() == By.CLASS_NAME:
        locator_value = f".{locator_value}"
        locator_type = By.CSS_SELECTOR
        return locator_type, locator_value

    if locator_type.lower() == By.NAME:
        locator_value = f"[name='{locator_value}']"
        locator_type = By.CSS_SELECTOR
        return locator_type, locator_value

    if locator_type.lower() == By.XPATH:
        try:
            locator_value = cssify(locator_value)
            locator_type = By.CSS_SELECTOR
            return locator_type, locator_value
        except Exception:
            # just ignore it and keep using the xpath selector
            pass

    # default path
    return locator_type, locator_value
