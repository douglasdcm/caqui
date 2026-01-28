# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui.cdp.engine import asynchronous

if TYPE_CHECKING:
    from caqui.cdp.asynchronous.drivers import AsyncDriverCDP


class Alert:
    def __init__(self, driver: "AsyncDriverCDP") -> None:
        self._conn = driver.conn
        self._current_element = driver._current_element.element_id

    async def get_text(self) -> str:
        """Returns the text of the alert"""
        return await asynchronous.get_alert_text(self._conn, self._current_element)

    async def accept(self) -> None:
        """Accepts the alert"""
        await asynchronous.accept_alert(self._conn, self._current_element)

    async def dismiss(self) -> None:
        """Closes the alert ignoring it"""
        await asynchronous.dismiss_alert(self._conn, self._current_element)

    async def send_keys(self, text) -> None:
        """Send a text to a textbox in the alert and closes it"""
        await asynchronous.send_alert_text(
            conn=self._conn, text=text, alert_element=self._current_element
        )
