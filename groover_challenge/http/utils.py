# -*- coding: utf-8 -*-

from requests.exceptions import ConnectionError
from rest_framework.views import exception_handler

from .exceptions import ConnectionErrorException

ERRORS_MAP = {
    ConnectionError: ConnectionErrorException
}


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
    return response


def http_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            e_type = type(e)
            if e_type in ERRORS_MAP:
                raise ERRORS_MAP[e_type]
            raise e
    return inner
