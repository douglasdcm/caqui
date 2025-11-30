from caqui import asynchronous


class Window:
    def __init__(self, driver) -> None:
        self._remote = driver.remote
        self._ssession = driver.session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self._remote, self._session, window_type)
