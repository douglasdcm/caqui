from caqui import asynchronous


class ActionChains:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session
        self.__coroutines = []
        self.__element = None

    def click(self, element=None):
        if not element:
            element = self.__element
        coroutine = asynchronous.click(self.__remote, self.__session, str(element))
        self.__coroutines.append(coroutine)
        return self

    def move_to_element(self, element):
        self.__element = element
        coroutine = asynchronous.actions_move_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element):
        self.__element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    async def perform(self):
        for coroutine in self.__coroutines:
            await coroutine
        return True
