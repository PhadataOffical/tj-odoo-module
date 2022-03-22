
SUCCESS = '200000'
HTTP_OK = 200


class ApiResult(object):
    """
    API Result
    """
    code = str
    message = str
    payload = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return None


def parser(json_data) -> ApiResult:
    d = ApiResult.__new__(ApiResult)
    d.__dict__.update(json_data)
    return d
