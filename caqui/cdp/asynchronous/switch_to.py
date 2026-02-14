# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, Union

from caqui._vendor.chrome_devtools_protocol.cdp import dom, target

from caqui.cdp.asynchronous.alert import Alert
from caqui.cdp.asynchronous.element import Element
from caqui.cdp.engine import asynchronous

if TYPE_CHECKING:
    from caqui.cdp.asynchronous.drivers import AsyncDriverCDP


class SwitchTo:
    def __init__(self, driver: "AsyncDriverCDP") -> None:
        self._driver = driver
        self._iframe: dom.NodeId = None
        self._window_handle: Union[str] = ""

    # TODO test it
    @property
    def alert(self) -> "Alert":
        """Returns the `Alert` object"""
        return Alert(self._driver)

    async def get_active_element(self) -> "Element":
        """Returns the active element"""
        element = await asynchronous.get_active_element(self._driver.conn)
        return Element(element, self._driver)

    async def new_window(self) -> str:
        """Opens a new window"""
        await asynchronous.new_window(
            self._driver.conn,
        )
        window_handle = (await asynchronous.get_window_handles(self._driver.conn))[0]
        await self.window(window_handle)
        return self._window_handle

    async def window(self, window_handle: target.TargetInfo) -> None:
        """Switchs to window `window_handle`"""
        new_conn = await asynchronous.switch_to_window(
            self._driver.conn,
            window_handle,
        )
        self._driver._conn = new_conn
        self._window_handle = window_handle

    async def frame(self, iframe: dom.NodeId) -> None:
        """Switches to frame `iframe`"""
        self._iframe = iframe.element_id
        await asynchronous.switch_to_frame(
            self._driver.conn,
            self._iframe,
        )

    # TODO test it
    async def default_content(self) -> None:
        """Switches to parent frame of 'element_frame'"""
        await asynchronous.switch_to_parent_frame(
            self._driver.conn,
            # self._iframe,
        )
