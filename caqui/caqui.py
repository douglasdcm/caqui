from caqui import asynchronous, synchronous


class Element:
    def __init__(self, element, remote, session) -> None:
        self.__element = element
        self.__remote = remote
        self.__session = session

    @property
    def element(self):
        return self.__element

    async def get_computed_label(self):
        return await asynchronous.get_computed_label(
            self.__remote, self.__session, self.__element
        )

    async def get_attribute(self, attribute):
        return await asynchronous.get_attribute(
            self.__remote, self.__session, self.__element, attribute
        )

    async def clear(self):
        return await asynchronous.clear_element(
            self.__remote, self.__session, self.__element
        )

    async def send_keys(self, text):
        return await asynchronous.send_keys(
            self.__remote, self.__session, self.__element, text
        )

    async def click(self):
        return await asynchronous.click(self.__remote, self.__session, self.__element)

    async def find_elements(self, locator, value):
        return await asynchronous.find_children_elements(
            self.__remote, self.__session, self.__element, locator, value
        )

    async def find_element(self, locator, value):
        return await asynchronous.find_child_element(
            self.__remote, self.__session, self.__element, locator, value
        )


class AsyncDriver:
    def __init__(self, remote, capabilities, url) -> None:
        self.__remote = remote
        self.__session = synchronous.get_session(remote, capabilities)
        synchronous.get(
            remote,
            self.__session,
            url,
        )

    def quit(self):
        synchronous.close_session(self.__remote, self.__session)

    async def get(self, url):
        await asynchronous.go_to_page(
            self.__remote,
            self.__session,
            url,
        )

    async def find_elements(self, locator, value):
        elements = await asynchronous.find_elements(
            self.__remote, self.__session, locator, value
        )
        result = []
        for element in elements:
            result.append(Element(element, self.__remote, self.__session))
        return result

    async def find_element(self, locator, value):
        element = await asynchronous.find_element(
            self.__remote, self.__session, locator, value
        )
        return Element(element, self.__remote, self.__session)
