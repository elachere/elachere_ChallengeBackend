# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from rest_framework import status


class ConnectionErrorException(APIException):
    """
    Exception to raise when connection is failing.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Server could not establish connection to spotify.'
    default_code = 'no_connection'

    def __init__(self, detail=None, **kwargs):
        detail = detail or self.default_detail
        code = self.default_code
        super().__init__(detail=detail, code=code, **kwargs)


class TimeOutException(APIException):
    """
    Exception to raise when connection timed out.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Connection to spotify api timed out.'
    default_code = 'time_out'

    def __init__(self, detail=None, **kwargs):
        detail = detail or self.default_detail
        code = self.default_code
        super().__init__(detail=detail, code=code, **kwargs)


class SSLException(APIException):
    """
    Exception to raise when ssl handshake failed.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'SSL handshake failed. May be spotify admins forgot to renew certs.'
    default_code = 'ssl_error'

    def __init__(self, detail=None, **kwargs):
        detail = detail or self.default_detail
        code = self.default_code
        super().__init__(detail=detail, code=code, **kwargs)
