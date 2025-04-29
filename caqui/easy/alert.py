from caqui import asynchronous, synchronous


class Alert:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session

    @property
    def text(self):
        """Returns the text of the alert"""
        return synchronous.get_alert_text(self.__remote, self.__session)

    async def accept(self):
        """Accepts the alert"""
        return await asynchronous.accept_alert(self.__remote, self.__session)

    async def dismiss(self):
        """Closes the alert ignoring it"""
        return await asynchronous.dismiss_alert(self.__remote, self.__session)

    async def send_keys(self, text):
        """Send a text to a textbox in the alert"""
        return await asynchronous.send_alert_text(self.__remote, self.__session, text)
