# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui.cdp.engine import synchronous

if TYPE_CHECKING:
    from caqui.cdp.synchronous.drivers import SyncDriverCDP


class Window:
    def __init__(self, driver: "SyncDriverCDP") -> None:
        self._session = driver.conn
        self._driver = driver

    # TODO test it
    def new(self) -> str:
        """
        Open a new window
        return (str): window handle
        """
        synchronous.new_window(self._session)
        return (synchronous.get_window_handles(self._driver.conn))[0]
