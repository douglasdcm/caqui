from caqui import asynchronous, synchronous
from caqui.easy.element import Element
from caqui.easy.alert import Alert


class SwitchTo:
    def __init__(self, driver) -> None:
        self.__driver = driver
        self.__iframe = None
        self.__window_handle = None

    @property
    def active_element(self):
        """Returns the active element"""
        element = synchronous.get_active_element(self.__driver.remote, self.__driver.session)
        return Element(element, self.__driver)

    @property
    def alert(self):
        """Returns the `Alert` object"""
        return Alert(self.__driver)

    async def new_window(self, window_type):
        """Opens a new window"""
        self.__window_handle = await asynchronous.new_window(
            self.__driver.remote, self.__driver.session, window_type
        )
        self.__window_handle = await asynchronous.switch_to_window(
            self.__driver.remote, self.__driver.session, self.__window_handle
        )
        return self.__window_handle

    async def window(self, window_handle):
        """Switchs to window `window_handle`"""
        self.__window_handle = await asynchronous.switch_to_window(
            self.__driver.remote, self.__driver.session, window_handle
        )
        return self.__window_handle

    async def frame(self, iframe):
        """Switches to frame `iframe`"""
        self.__iframe = str(iframe)
        return await asynchronous.switch_to_frame(
            self.__driver.remote, self.__driver.session, self.__iframe
        )

    async def default_content(self):
        """Switches to parent frame of 'element_frame'"""
        return await asynchronous.switch_to_parent_frame(
            self.__driver.remote, self.__driver.session, self.__iframe
        )
