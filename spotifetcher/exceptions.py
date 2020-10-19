# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException
from rest_framework import status


class ConnectionErrorException(APIException):
    """
    Exception to raise when a parameter is missing in a POST API call.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Contact you`\re internet provider.'
    default_code = 'no_connection'

    def __init__(self, detail=None, **kwargs):
        detail = detail or self.default_detail
        code = self.default_code
        super().__init__(detail=detail, code=code, **kwargs)
