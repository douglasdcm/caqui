# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui.cdp.engine import synchronous

if TYPE_CHECKING:
    from caqui.cdp.synchronous.drivers import SyncDriverCDP


class Alert:
    def __init__(self, driver: "SyncDriverCDP") -> None:
        self._conn = driver.conn
        self._current_element = driver._current_element.element_id

    def get_text(self) -> str:
        """Returns the text of the alert"""
        return synchronous.get_alert_text(self._conn, self._current_element)

    def accept(self) -> None:
        """Accepts the alert"""
        synchronous.accept_alert(self._conn, self._current_element)

    def dismiss(self) -> None:
        """Closes the alert ignoring it"""
        synchronous.dismiss_alert(self._conn, self._current_element)

    def send_keys(self, text) -> None:
        """Send a text to a textbox in the alert and closes it"""
        synchronous.send_alert_text(conn=self._conn, text=text, alert_element=self._current_element)
