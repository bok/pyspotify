import ctypes as _ctypes
import os as _os

from spotify.capi import *

SPOTIFY_API_VERSION = 12

if _os.environ.get('USE_LIBMOCKSPOTIFY'):
    _libmockspotify = _ctypes.CDLL('libmockspotify.so.%s' % SPOTIFY_API_VERSION)
else:
    raise RuntimeError("Not using libmockspotify")

### Session

_mocksp_session_create = _libmockspotify.mocksp_session_create
_mocksp_session_create.argtypes = [_ctypes.POINTER(sp_session_config),
        sp_connectionstate, _ctypes.c_int,
        _ctypes.POINTER(sp_offline_sync_status),
        _ctypes.c_int, _ctypes.c_int, _ctypes.POINTER(sp_playlist)]
_mocksp_session_create.restype = _ctypes.POINTER(sp_session)

def mocksp_session_create(config=None,
        connection_state=SP_CONNECTION_STATE_LOGGED_OUT, offline_time_left=0,
        sync_status=None, offline_num_playlists=0, offline_tracks_to_sync=0,
        inbox=None, user=None, scrobbling_possible=0):
    if config is None:
        config = sp_session_config()
    return _mocksp_session_create(config, connection_state, offline_time_left,
            sync_status, offline_num_playlists, offline_tracks_to_sync,
            inbox, user, scrobbling_possible)

_mocksp_session_destroy = _libmockspotify.mocksp_session_destroy
_mocksp_session_destroy.argtypes = [_ctypes.POINTER(sp_session)]
_mocksp_session_destroy.restype = None

def mocksp_session_destroy(session):
    _mocksp_session_destroy(session)
