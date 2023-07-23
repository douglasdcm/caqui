from caqui import asynchronous


class Window:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self.__remote, self.__session, window_type)
