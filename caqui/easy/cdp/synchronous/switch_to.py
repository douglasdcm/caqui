# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, Union

from caqui.cdp import synchronous
from caqui.easy.cdp.synchronous.alert import Alert
from caqui.easy.cdp.synchronous.element import Element

if TYPE_CHECKING:
    from caqui.easy.cdp.synchronous.drivers import SyncDriverCDP


class SwitchTo:
    def __init__(self, driver: "SyncDriverCDP") -> None:
        self._driver = driver
        self._iframe: Union[str] = ""
        self._window_handle: Union[str] = ""

    # TODO test it
    @property
    def alert(self) -> "Alert":
        """Returns the `Alert` object"""
        return Alert(self._driver)

    def get_active_element(self) -> "Element":
        """Returns the active element"""
        element = synchronous.get_active_element(self._driver.conn)
        return Element(element, self._driver)

    def new_window(self) -> str:
        """Opens a new window"""
        synchronous.new_window(
            self._driver.conn,
        )
        window_handle = (synchronous.get_window_handles(self._driver.conn))[0]
        self.window(window_handle)
        return self._window_handle

    def window(self, window_handle: str) -> str:
        """Switchs to window `window_handle`"""
        new_conn = synchronous.switch_to_window(
            self._driver.conn,
            window_handle,
        )
        self._driver._conn = new_conn
        self._window_handle = window_handle

    def frame(self, iframe: Union[str, Element]) -> None:
        """Switches to frame `iframe`"""
        self._iframe = iframe.element_id
        synchronous.switch_to_frame(
            self._driver.conn,
            self._iframe,
        )

    # TODO test it
    def default_content(self) -> None:
        """Switches to parent frame of 'element_frame'"""
        synchronous.switch_to_parent_frame(
            self._driver.conn,
            self._iframe,
        )
