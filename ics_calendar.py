import base64
from urllib import parse

import requests
from ics import Calendar as CalendarBase


class Calendar(CalendarBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_remote(cls, location, authorization=""):
        url = cls.__authorised_url(location, authorization)
        return cls(requests.get(url).text)

    @staticmethod
    def __authorised_url(location, auth):
        url = parse.urlparse(location)
        if auth:
            auth = base64.b64decode(auth.encode()).decode()
            url = url._replace(netloc="{}@{}".format(auth, url.netloc))

        return parse.urlunparse(url)

    @property
    def title(self):
        if self._unused:
            return self._unused[0].value
        return ""
