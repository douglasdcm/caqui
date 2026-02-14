import datetime
from time import sleep
from asyncio import sleep as async_sleep
from typing import Callable, Coroutine
from caqui.constants import TIMEOUT


class WebDriverWait:
    def __init__(self, driver, timeout=TIMEOUT, pooling_time=0.5):
        self._driver = driver
        self._timeout = timeout
        self._pooling_time = pooling_time

    def until(self, condition: Callable):
        """Waits a condition be true or raises a TimeoutError exception"""
        current_datetime = datetime.datetime.now()
        time_to_add = datetime.timedelta(seconds=self._timeout)
        new_datetime = current_datetime + time_to_add
        while datetime.datetime.now() < new_datetime:
            if condition():
                return
            sleep(self._pooling_time)
        raise TimeoutError()
    
    async def async_until(self, condition: Coroutine):
        """Waits a condition be true or raises a TimeoutError exception"""
        current_datetime = datetime.datetime.now()
        time_to_add = datetime.timedelta(seconds=self._timeout)
        new_datetime = current_datetime + time_to_add
        while datetime.datetime.now() < new_datetime:
            if await condition():
                return
            await async_sleep(self._pooling_time)
        raise TimeoutError()