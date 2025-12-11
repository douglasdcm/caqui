# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, Union

from caqui import asynchronous, synchronous
from caqui.easy.alert import Alert
from caqui.easy.element import Element

if TYPE_CHECKING:
    from caqui.easy.drivers import AsyncDriver


class SwitchToW3C:
    def __init__(self, driver: "AsyncDriver") -> None:
        self._driver = driver
        self._iframe: Union[str] = ""
        self._window_handle: Union[str] = ""
        self._session_http = driver.session_http

    @property
    def active_element(self) -> "Element":
        """Returns the active element"""
        element = synchronous.get_active_element(self._driver.server_url, self._driver.session)
        return Element(element, self._driver)

    @property
    def alert(self) -> "Alert":
        """Returns the `Alert` object"""
        return Alert(self._driver)

    async def new_window(self, window_type) -> str:
        """Opens a new window"""
        self._window_handle = await asynchronous.new_window(
            self._driver.server_url,
            self._driver.session,
            window_type,
            session_http=self._session_http,
        )
        self._window_handle = await asynchronous.switch_to_window(
            self._driver.server_url,
            self._driver.session,
            self._window_handle,
            session_http=self._session_http,
        )
        return self._window_handle

    async def window(self, window_handle: str) -> str:
        """Switchs to window `window_handle`"""
        self._window_handle = await asynchronous.switch_to_window(
            self._driver.server_url,
            self._driver.session,
            window_handle,
            session_http=self._session_http,
        )
        return self._window_handle

    async def frame(self, iframe: Union[str, Element]) -> None:
        """Switches to frame `iframe`"""
        self._iframe = str(iframe)
        await asynchronous.switch_to_frame(
            self._driver.server_url,
            self._driver.session,
            self._iframe,
            session_http=self._session_http,
        )

    async def default_content(self) -> None:
        """Switches to parent frame of 'element_frame'"""
        await asynchronous.switch_to_parent_frame(
            self._driver.server_url,
            self._driver.session,
            self._iframe,
            session_http=self._session_http,
        )


class SwitchToJsonWire(SwitchToW3C):
    def __init__(self, driver) -> None:
        super().__init__(driver)
        self._driver = driver
        self._iframe: Union[str] = ""
        self._window_handle: Union[str] = ""
        self._session_http = driver.session_http

    @property
    def active_element(self):
        """Returns the active element"""
        element = synchronous.get_active_element_jsonwire(
            self._driver.server_url, self._driver.session
        )
        return Element(element, self._driver)

    async def new_window(self, window_type):
        """Opens a new window"""
        self._window_handle = await asynchronous.new_window(
            self._driver.server_url,
            self._driver.session,
            window_type,
            session_http=self._session_http,
        )
        self._window_handle = await asynchronous.switch_to_window_jsonwire(
            self._driver.server_url,
            self._driver.session,
            self._window_handle,
            session_http=self._session_http,
        )
        return self._window_handle

    async def window(self, window_handle):
        """Switchs to window `window_handle`"""
        self._window_handle = await asynchronous.switch_to_window_jsonwire(
            self._driver.server_url,
            self._driver.session,
            window_handle,
            session_http=self._session_http,
        )
        return self._window_handle

    async def default_content(self):
        """Switches to parent frame of 'element_frame'"""
        return await asynchronous.switch_to_parent_frame_jsonwire(
            self._driver.server_url,
            self._driver.session,
            self._iframe,
            session_http=self._session_http,
        )

    async def frame(self, iframe):
        """Switches to frame `iframe`"""
        self._iframe = str(iframe)
        return await asynchronous.switch_to_frame_jsonwire(
            self._driver.server_url,
            self._driver.session,
            self._iframe,
            session_http=self._session_http,
        )
