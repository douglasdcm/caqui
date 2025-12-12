# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING

from caqui import asynchronous

if TYPE_CHECKING:
    from caqui.easy.drivers import AsyncDriver


class Window:
    def __init__(self, driver: "AsyncDriver") -> None:
        self.server_url = driver.server_url
        self._session = driver.session

    async def new(self, window_type: str = "tab") -> str:
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self.server_url, self._session, window_type)
