
from spotify.mock import capi as mockapi

def _mockapi_func(prefix, method):
    return mockapi.__getattribute__('mocksp_{prefix}_{method}'.format(
                                    prefix=prefix, method=method))

class MockSpotifyObject(object):

    def __init__(self, *args, **kwargs):
        # Define _as_parameter_ to be able to pass this object to capi functions
        self._as_parameter_ = _mockapi_func(self._prefix, 'create')(*args, **kwargs)

    def __del__(self):
        _mockapi_func(self._prefix, 'destroy')(self)
