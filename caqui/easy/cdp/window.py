# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui.cdp import asynchronous

if TYPE_CHECKING:
    from caqui.easy.cdp.drivers import AsyncDriver


class Window:
    def __init__(self, driver: "AsyncDriver") -> None:
        self._session = driver.conn

    # TODO test it
    async def new(self) -> str:
        """
        Open a new window
        return (str): window handle
        """
        await asynchronous.new_window()
        return (await asynchronous.get_window_handles(self._driver.conn))[0]
