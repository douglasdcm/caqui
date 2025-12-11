# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui


from typing import Dict

HEADERS: Dict[str, str] = {
    "Accept-Encoding": "identity",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "keep-alive",
}
ELEMENT_W3C: str = "element-6066-11e4-a52e-4f735466cecf"
ELEMENT_JSONWIRE: str = "ELEMENT"


class Specification:
    CHROME: str = "ChromeCapabilitiesBuilder"
    FIREFOX: str = "FirefoxCapabilitiesBuilder"
    EDGE: str = "EdgeCapabilitiesBuilder"
    OPERA: str = "OperaCapabilitiesBuilder"
    JSONWIRE: str = "jsonwire"
    W3C: str = "w3c"
