# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui


class By:
    """List of locator strategies"""

    CSS_SELECTOR: str = "css selector"
    ID: str = "id"
    XPATH: str = "xpath"
    NAME: str = "name"
    TAG_NAME: str = "tag name"
    CLASS_NAME: str = "class name"
    LINK_TEXT: str = "link text"
    PARTIAL_LINK_TEXT: str = "partial link text"
