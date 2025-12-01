# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from caqui import asynchronous


class Window:
    def __init__(self, driver) -> None:
        self._remote = driver.remote
        self._session = driver.session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self._remote, self._session, window_type)
