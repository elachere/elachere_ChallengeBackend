# -*- coding: utf-8 -*-
from requests import Session
from urllib.parse import urljoin


class BaseUrlSession(Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if base_url:
            self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        return super().request(method, url, *args, **kwargs)
