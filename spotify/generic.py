
from spotify import capi

def _capi_func(prefix, method):
    return capi.__getattribute__('sp_{prefix}_{method}'.format(
                                 prefix=prefix, method=method))

class SpotifyObject(object):

    def __init__(self):
        self._as_parameter_ = None

    @classmethod
    def _from_cdata(cls, pointer, add_ref=True):
        """
        Create the object from a CAPI cdata.

        If add_ref is True, sp_<type>_add_ref() is called on the newly created
        instance.
        """
        self = cls()
        self._as_parameter_ = pointer
        if add_ref:
            _capi_func(cls._prefix, 'add_ref')(self)
        return self

    def __del__(self):
        """
        Calls sp_<type>_release() on the object before deletion.
        """
        if self._as_parameter_ is not None:
            _capi_func(self._prefix, 'release')(self)

