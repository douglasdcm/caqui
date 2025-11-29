from caqui import asynchronous, synchronous


class Alert:
    def __init__(self, driver) -> None:
        self._remote = driver.remote
        self._session = driver.session
        self._session_http = driver.session_http

    @property
    def text(self):
        """Returns the text of the alert"""
        return synchronous.get_alert_text(self._remote, self._session)

    async def accept(self):
        """Accepts the alert"""
        return await asynchronous.accept_alert(
            self._remote, self._session, session_http=self._session_http
        )

    async def dismiss(self):
        """Closes the alert ignoring it"""
        return await asynchronous.dismiss_alert(
            self._remote, self._session, session_http=self._session_http
        )

    async def send_keys(self, text):
        """Send a text to a textbox in the alert"""
        return await asynchronous.send_alert_text(
            self._remote, self._session, text, session_http=self._session_http
        )
