# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui import asynchronous, synchronous

if TYPE_CHECKING:
    from caqui.easy.drivers import AsyncDriver


class Alert:
    def __init__(self, driver: "AsyncDriver") -> None:
        self._server_url = driver.server_url
        self._session = driver.session
        self._session_http = driver.session_http

    @property
    def text(self) -> str:
        """Returns the text of the alert"""
        return synchronous.get_alert_text(self._server_url, self._session)

    async def accept(self) -> None:
        """Accepts the alert"""
        await asynchronous.accept_alert(
            self._server_url, self._session, session_http=self._session_http
        )

    async def dismiss(self) -> None:
        """Closes the alert ignoring it"""
        await asynchronous.dismiss_alert(
            self._server_url, self._session, session_http=self._session_http
        )

    async def send_keys(self, text) -> None:
        """Send a text to a textbox in the alert"""
        await asynchronous.send_alert_text(
            self._server_url, self._session, text, session_http=self._session_http
        )
