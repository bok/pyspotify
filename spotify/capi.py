import os as _os
import ctypes as _ctypes
from functools import wraps

SPOTIFY_API_VERSION = 12

if _os.environ.get('USE_LIBMOCKSPOTIFY'):
    _libspotify = _ctypes.CDLL('libmockspotify.so.%s' % SPOTIFY_API_VERSION)
else:
    _libspotify = _ctypes.CDLL('libspotify.so.%s' % SPOTIFY_API_VERSION)

### Spotify types & structs

sp_uint64 = _ctypes.c_uint64
sp_bool = _ctypes.c_ubyte

class sp_session(_ctypes.Structure):
    pass

class sp_track(_ctypes.Structure):
    pass

class sp_album(_ctypes.Structure):
    pass

class sp_artist(_ctypes.Structure):
    pass

class sp_artistbrowse(_ctypes.Structure):
    pass

class sp_albumbrowse(_ctypes.Structure):
    pass

class sp_toplistbrowse(_ctypes.Structure):
    pass

class sp_search(_ctypes.Structure):
    pass

class sp_link(_ctypes.Structure):
    pass

class sp_image(_ctypes.Structure):
    pass

class sp_user(_ctypes.Structure):
    pass

class sp_playlist(_ctypes.Structure):
    pass

class sp_playlistcontainer(_ctypes.Structure):
    pass

class sp_inbox(_ctypes.Structure):
    pass


### Error handling

sp_error = _ctypes.c_int

SP_ERROR_OK = 0
SP_ERROR_BAD_API_VERSION = 1
SP_ERROR_API_INITIALIZATION_FAILED = 2
SP_ERROR_TRACK_NOT_PLAYABLE = 3
SP_ERROR_BAD_APPLICATION_KEY = 5
SP_ERROR_BAD_USERNAME_OR_PASSWORD = 6
SP_ERROR_USER_BANNED = 7
SP_ERROR_UNABLE_TO_CONTACT_SERVER = 8
SP_ERROR_CLIENT_TOO_OLD = 9
SP_ERROR_OTHER_PERMANENT = 10
SP_ERROR_BAD_USER_AGENT = 11
SP_ERROR_MISSING_CALLBACK = 12
SP_ERROR_INVALID_INDATA = 13
SP_ERROR_INDEX_OUT_OF_RANGE = 14
SP_ERROR_USER_NEEDS_PREMIUM = 15
SP_ERROR_OTHER_TRANSIENT = 16
SP_ERROR_IS_LOADING = 17
SP_ERROR_NO_STREAM_AVAILABLE = 18
SP_ERROR_PERMISSION_DENIED = 19
SP_ERROR_INBOX_IS_FULL = 20
SP_ERROR_NO_CACHE = 21
SP_ERROR_NO_SUCH_USER = 22
SP_ERROR_NO_CREDENTIALS = 23
SP_ERROR_NETWORK_DISABLED = 24
SP_ERROR_INVALID_DEVICE_ID = 25
SP_ERROR_CANT_OPEN_TRACE_FILE = 26
SP_ERROR_APPLICATION_BANNED = 27
SP_ERROR_OFFLINE_TOO_MANY_TRACKS = 31
SP_ERROR_OFFLINE_DISK_CACHE = 32
SP_ERROR_OFFLINE_EXPIRED = 33
SP_ERROR_OFFLINE_NOT_ALLOWED = 34
SP_ERROR_OFFLINE_LICENSE_LOST = 35
SP_ERROR_OFFLINE_LICENSE_ERROR = 36
SP_ERROR_LASTFM_AUTH_ERROR = 39
SP_ERROR_INVALID_ARGUMENT = 40
SP_ERROR_SYSTEM_FAILURE = 41

_sp_error_message = _libspotify.sp_error_message
_sp_error_message.argtypes = [sp_error]
_sp_error_message.restype = _ctypes.c_char_p

def sp_error_message(error):
    return _sp_error_message(error).decode('utf-8')

class SpError(Exception):
    def __init__(self, sp_error):
        super(SpError, self).__init__('%s (error %d)' % (
            sp_error_message(sp_error), sp_error))
        self.code = sp_error

# Decorator for API function returning sp_error: we return None and raise SpError if
# the return value is != SP_ERROR_OK
def returns_sp_error(sp_func):
    @wraps(sp_func)
    def wrapper(*args, **kwds):
        error = sp_func(*args, **kwds)
        if error != SP_ERROR_OK:
            raise SpError(error)
    return wrapper

### Session handling

sp_connectionstate = _ctypes.c_int

SP_CONNECTION_STATE_LOGGED_OUT = 0
SP_CONNECTION_STATE_LOGGED_IN = 1
SP_CONNECTION_STATE_DISCONNECTED = 2
SP_CONNECTION_STATE_UNDEFINED = 3
SP_CONNECTION_STATE_OFFLINE = 4

sp_sampletype = _ctypes.c_int

SP_SAMPLETYPE_INT16_NATIVE_ENDIAN = 0

class sp_audioformat(_ctypes.Structure):
    _fields_ = [
        ('sample_type', sp_sampletype),
        ('sample_rate', _ctypes.c_int),
        ('channels', _ctypes.c_int),
    ]

sp_bitrate = _ctypes.c_int

SP_BITRATE_160k = 0
SP_BITRATE_320k = 1
SP_BITRATE_96k = 2

SP_PLAYLIST_TYPE_PLAYLIST = 0
SP_PLAYLIST_TYPE_START_FOLDER = 1
SP_PLAYLIST_TYPE_END_FOLDER = 2
SP_PLAYLIST_TYPE_PLACEHOLDER = 3

sp_search_type = _ctypes.c_int

SP_SEARCH_STANDARD = 0
SP_SEARCH_SUGGEST = 1

SP_PLAYLIST_OFFLINE_STATUS_NO = 0
SP_PLAYLIST_OFFLINE_STATUS_YES = 1
SP_PLAYLIST_OFFLINE_STATUS_DOWNLOADING = 2
SP_PLAYLIST_OFFLINE_STATUS_WAITING = 3

sp_track_availability = _ctypes.c_int

SP_TRACK_AVAILABILITY_UNAVAILABLE = 0
SP_TRACK_AVAILABILITY_AVAILABLE = 1
SP_TRACK_AVAILABILITY_NOT_STREAMABLE = 2
SP_TRACK_AVAILABILITY_BANNED_BY_ARTIST = 3

sp_track_offline_status = _ctypes.c_int

SP_TRACK_OFFLINE_NO = 0
SP_TRACK_OFFLINE_WAITING = 1
SP_TRACK_OFFLINE_DOWNLOADING = 2
SP_TRACK_OFFLINE_DONE = 3
SP_TRACK_OFFLINE_ERROR = 4
SP_TRACK_OFFLINE_DONE_EXPIRED = 5
SP_TRACK_OFFLINE_LIMIT_EXCEEDED = 6
SP_TRACK_OFFLINE_DONE_RESYNC = 7

sp_image_size = _ctypes.c_int

SP_IMAGE_SIZE_NORMAL = 0
SP_IMAGE_SIZE_SMALL = 1
SP_IMAGE_SIZE_LARGE = 2

class sp_audio_buffer_stats(_ctypes.Structure):
    _fields_ = [
        ('samples', _ctypes.c_int),
        ('stutter', _ctypes.c_int),
    ]

class sp_subscribers(_ctypes.Structure):
    _fields_ = [
        ('count', _ctypes.c_int),
        ('subscribers', _ctypes.POINTER(_ctypes.c_char_p)),
    ]

sp_connection_type = _ctypes.c_int

SP_CONNECTION_TYPE_UNKNOWN = 0
SP_CONNECTION_TYPE_NONE = 1
SP_CONNECTION_TYPE_MOBILE = 2
SP_CONNECTION_TYPE_MOBILE_ROAMING = 3
SP_CONNECTION_TYPE_WIFI = 4
SP_CONNECTION_TYPE_WIRED = 5

sp_connection_rules = _ctypes.c_int

SP_CONNECTION_RULE_NETWORK = 0x1
SP_CONNECTION_RULE_NETWORK_IF_ROAMING = 0x2
SP_CONNECTION_RULE_ALLOW_SYNC_OVER_MOBILE = 0x4
SP_CONNECTION_RULE_ALLOW_SYNC_OVER_WIFI = 0x8

sp_artistbrowse_type = _ctypes.c_int

SP_ARTISTBROWSE_FULL = 0
SP_ARTISTBROWSE_NO_TRACKS = 1
SP_ARTISTBROWSE_NO_ALBUMS = 2

sp_social_provider = _ctypes.c_int

SP_SOCIAL_PROVIDER_SPOTIFY  = 0
SP_SOCIAL_PROVIDER_FACEBOOK = 1
SP_SOCIAL_PROVIDER_LASTFM   = 2

sp_scrobbling_state = _ctypes.c_int

SP_SCROBBLING_STATE_USE_GLOBAL_SETTING    = 0
SP_SCROBBLING_STATE_LOCAL_ENABLED         = 1
SP_SCROBBLING_STATE_LOCAL_DISABLED        = 2
SP_SCROBBLING_STATE_GLOBAL_ENABLED        = 3
SP_SCROBBLING_STATE_GLOBAL_DISABLED       = 4

class sp_offline_sync_status(_ctypes.Structure):
    _fields_ = [
        ('queued_tracks', _ctypes.c_int),
        ('queued_bytes', _ctypes.c_uint64),
        ('done_tracks', _ctypes.c_int),
        ('done_bytes', _ctypes.c_uint64),
        ('copied_tracks', _ctypes.c_int),
        ('copied_bytes', _ctypes.c_uint64),
        ('willnotcopy_tracks', _ctypes.c_int),
        ('error_tracks', _ctypes.c_int),
        ('syncing', sp_bool),
    ]

SP_SESSION_LOGGED_IN_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_error)

SP_SESSION_LOGGED_OUT_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_METADATA_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_CONNECTION_ERROR_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_error)

SP_SESSION_MESSAGE_TO_USER_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), _ctypes.c_char_p)

SP_SESSION_NOTIFY_MAIN_THREAD_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_MUSIC_DELIVERY_FUNC = _ctypes.CFUNCTYPE(_ctypes.c_int,
    _ctypes.POINTER(sp_session), _ctypes.POINTER(sp_audioformat),
    _ctypes.c_void_p, _ctypes.c_int)

SP_SESSION_PLAY_TOKEN_LOST_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_LOG_MESSAGE_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), _ctypes.c_char_p)

SP_SESSION_END_OF_TRACK_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_STREAMING_ERROR_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_error)

SP_SESSION_USERINFO_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_START_PLAYBACK_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_STOP_PLAYBACK_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_GET_AUDIO_BUFFER_STATS_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), _ctypes.POINTER(sp_audio_buffer_stats))

SP_SESSION_OFFLINE_STATUS_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_OFFLINE_ERROR_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_error)

SP_SESSION_CREDENTIALS_BLOB_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), _ctypes.c_char_p)

SP_SESSION_CONNECTIONSTATE_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session))

SP_SESSION_SCROBBLE_ERROR_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_error)

SP_SESSION_PRIVATE_SESSION_MODE_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_session), sp_bool)

class sp_session_callbacks(_ctypes.Structure):
    _fields_ = [
        ('logged_in', SP_SESSION_LOGGED_IN_FUNC),
        ('logged_out', SP_SESSION_LOGGED_OUT_FUNC),
        ('metadata_updated', SP_SESSION_METADATA_UPDATED_FUNC),
        ('connection_error', SP_SESSION_CONNECTION_ERROR_FUNC),
        ('message_to_user', SP_SESSION_MESSAGE_TO_USER_FUNC),
        ('notify_main_thread', SP_SESSION_NOTIFY_MAIN_THREAD_FUNC),
        ('music_delivery', SP_SESSION_MUSIC_DELIVERY_FUNC),
        ('play_token_lost', SP_SESSION_PLAY_TOKEN_LOST_FUNC),
        ('log_message', SP_SESSION_LOG_MESSAGE_FUNC),
        ('end_of_track', SP_SESSION_END_OF_TRACK_FUNC),
        ('streaming_error', SP_SESSION_STREAMING_ERROR_FUNC),
        ('userinfo_updated', SP_SESSION_USERINFO_UPDATED_FUNC),
        ('start_playback', SP_SESSION_START_PLAYBACK_FUNC),
        ('stop_playback', SP_SESSION_STOP_PLAYBACK_FUNC),
        ('get_audio_buffer_stats', SP_SESSION_GET_AUDIO_BUFFER_STATS_FUNC),
        ('offline_status_updated', SP_SESSION_OFFLINE_STATUS_UPDATED_FUNC),
        ('offline_error', SP_SESSION_OFFLINE_ERROR_FUNC),
        ('credentials_blob_updated', SP_SESSION_CREDENTIALS_BLOB_UPDATED_FUNC),
        ('connectionstate_updated', SP_SESSION_CONNECTIONSTATE_UPDATED_FUNC),
        ('scrobble_error', SP_SESSION_SCROBBLE_ERROR_FUNC),
        ('private_session_mode_changed', SP_SESSION_PRIVATE_SESSION_MODE_CHANGED_FUNC),
    ]

class sp_session_config(_ctypes.Structure):
    _fields_ = [
        ('api_version', _ctypes.c_int),
        ('cache_location', _ctypes.c_char_p),
        ('settings_location', _ctypes.c_char_p),
        ('application_key', _ctypes.c_char_p),
        ('application_key_size', _ctypes.c_size_t),
        ('user_agent', _ctypes.c_char_p),
        ('callbacks', _ctypes.POINTER(sp_session_callbacks)),
        ('userdata', _ctypes.py_object),
        ('compress_playlists', sp_bool),
        ('dont_save_metadata_for_playlists', sp_bool),
        ('initially_unload_playlists', sp_bool),
        ('device_id', _ctypes.c_char_p),
        ('proxy', _ctypes.c_char_p),
        ('proxy_username', _ctypes.c_char_p),
        ('proxy_password', _ctypes.c_char_p),
        ('ca_certs_filename', _ctypes.c_char_p),
        ('tracefile', _ctypes.c_char_p),
    ]

_sp_session_create = _libspotify.sp_session_create
_sp_session_create.argtypes = [_ctypes.POINTER(sp_session_config),
     _ctypes.POINTER(_ctypes.POINTER(sp_session))]
_sp_session_create.restype = sp_error

def sp_session_create(config, callbacks):
    config.callbacks = _ctypes.pointer(callbacks)
    session = _ctypes.pointer(sp_session())
    error = _sp_session_create(_ctypes.byref(config), _ctypes.byref(session))
    if error == SP_ERROR_OK:
        return session
    else:
        raise SpError(error)

_sp_session_release = _libspotify.sp_session_release
_sp_session_release.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_release.restype = sp_error

@returns_sp_error
def sp_session_release(session):
    return _sp_session_release(session)

_sp_session_login = _libspotify.sp_session_login
_sp_session_login.argtypes = [_ctypes.POINTER(sp_session),
    _ctypes.c_char_p, _ctypes.c_char_p, sp_bool, _ctypes.c_char_p]
_sp_session_login.restype = sp_error

@returns_sp_error
def sp_session_login(session, username, password,
        remember_me=False, blob=None):
    return _sp_session_login(session, username.encode('utf-8'),
            password.encode('utf-8'), remember_me, blob)

_sp_session_relogin = _libspotify.sp_session_relogin
_sp_session_relogin.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_relogin.restype = sp_error

@returns_sp_error
def sp_session_relogin(session):
    return _sp_session_relogin(session)

_sp_session_remembered_user = _libspotify.sp_session_remembered_user
_sp_session_remembered_user.argtypes = [_ctypes.POINTER(sp_session),
    _ctypes.c_char_p, _ctypes.c_size_t]
_sp_session_remembered_user.restype = _ctypes.c_int

def sp_session_remembered_user(session):
    # First, we attempt to get the username length
    buf = (_ctypes.c_char * 1)()
    name_len = _sp_session_remembered_user(session, buf, 1)
    if name_len == -1:
        return None # No user stored

    buf = (_ctypes.c_char * (name_len + 1))()
    _sp_session_remembered_user(session, buf, name_len + 1)
    return buf.value.decode('utf-8')

_sp_session_user_name = _libspotify.sp_session_user_name
_sp_session_user_name.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_user_name.restype = _ctypes.c_char_p

def sp_session_user_name(session):
    return _sp_session_user_name(session).decode('utf-8')

_sp_session_forget_me = _libspotify.sp_session_forget_me
_sp_session_forget_me.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_forget_me.restype = sp_error

@returns_sp_error
def sp_session_forget_me(session):
    return _sp_session_forget_me(session)

_sp_session_user = _libspotify.sp_session_user
_sp_session_user.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_user.restype = _ctypes.POINTER(sp_user)

def sp_session_user(session):
    return _sp_session_user(session)

_sp_session_logout = _libspotify.sp_session_logout
_sp_session_logout.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_logout.restype = sp_error

@returns_sp_error
def sp_session_logout(session):
    return _sp_session_logout(session)

_sp_session_flush_caches = _libspotify.sp_session_flush_caches
_sp_session_flush_caches.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_flush_caches.restype = sp_error

@returns_sp_error
def sp_session_flush_caches(session):
    return _sp_session_flush_caches(session)

_sp_session_connectionstate = _libspotify.sp_session_connectionstate
_sp_session_connectionstate.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_connectionstate.restype = sp_connectionstate

def sp_session_connectionstate(session):
    return _sp_session_connectionstate(session)

_sp_session_userdata = _libspotify.sp_session_userdata
_sp_session_userdata.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_userdata.restype = _ctypes.py_object

def sp_session_userdata(session):
    return _sp_session_userdata(session)

_sp_session_set_cache_size = _libspotify.sp_session_set_cache_size
_sp_session_set_cache_size.argtypes = [_ctypes.POINTER(sp_session), _ctypes.c_size_t]
_sp_session_set_cache_size.restype = sp_error

@returns_sp_error
def sp_session_set_cache_size(session, size):
    return _sp_session_set_cache_size(session, size)

_sp_session_process_events = _libspotify.sp_session_process_events
_sp_session_process_events.argtypes = [_ctypes.POINTER(sp_session),
    _ctypes.POINTER(_ctypes.c_int)]
_sp_session_process_events.restype = sp_error

def sp_session_process_events(session):
    next_timeout = _ctypes.c_int(0)
    error = _sp_session_process_events(session, _ctypes.byref(next_timeout))
    if error == SP_ERROR_OK:
        return next_timeout.value
    else:
        raise SpError(error)

_sp_session_player_load = _libspotify.sp_session_player_load
_sp_session_player_load.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_session_player_load.restype = sp_error

@returns_sp_error
def sp_session_player_load(session, track):
    return _sp_session_player_load(session, track)

_sp_session_player_seek = _libspotify.sp_session_player_seek
_sp_session_player_seek.argtypes = [_ctypes.POINTER(sp_session), _ctypes.c_int]
_sp_session_player_seek.restype = sp_error

@returns_sp_error
def sp_session_player_seek(session, offset):
    return _sp_session_player_seek(session, offset)

_sp_session_player_play = _libspotify.sp_session_player_play
_sp_session_player_play.argtypes = [_ctypes.POINTER(sp_session), sp_bool]
_sp_session_player_play.restype = sp_error

@returns_sp_error
def sp_session_player_play(session, play):
    return _sp_session_player_play(session, play)

_sp_session_player_unload = _libspotify.sp_session_player_unload
_sp_session_player_unload.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_player_unload.restype = sp_error

@returns_sp_error
def sp_session_player_unload(session):
    return _sp_session_player_unload(session)

_sp_session_player_prefetch = _libspotify.sp_session_player_prefetch
_sp_session_player_prefetch.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_session_player_prefetch.restype = sp_error

@returns_sp_error
def sp_session_player_prefetch(session, track):
    return _sp_session_player_prefetch(session, track)

_sp_session_playlistcontainer = _libspotify.sp_session_playlistcontainer
_sp_session_playlistcontainer.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_playlistcontainer.restype = _ctypes.POINTER(sp_playlistcontainer)

def sp_session_playlistcontainer(session):
    return _sp_session_playlistcontainer(session)

_sp_session_inbox_create = _libspotify.sp_session_inbox_create
_sp_session_inbox_create.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_inbox_create.restype = _ctypes.POINTER(sp_playlist)

def sp_session_inbox_create(session):
    return _sp_session_inbox_create(session)

_sp_session_starred_create = _libspotify.sp_session_starred_create
_sp_session_starred_create.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_starred_create.restype = _ctypes.POINTER(sp_playlist)

def sp_session_starred_create(session):
    return _sp_session_starred_create(session)

_sp_session_starred_for_user_create = _libspotify.sp_session_starred_for_user_create
_sp_session_starred_for_user_create.argtypes = [_ctypes.POINTER(sp_session), _ctypes.c_char_p]
_sp_session_starred_for_user_create.restype = _ctypes.POINTER(sp_playlist)

def sp_session_starred_for_user_create(session, canonical_username):
    return _sp_session_starred_for_user_create(session, canonical_username)

_sp_session_publishedcontainer_for_user_create = _libspotify.sp_session_publishedcontainer_for_user_create
_sp_session_publishedcontainer_for_user_create.argtypes = [_ctypes.POINTER(sp_session), _ctypes.c_char_p]
_sp_session_publishedcontainer_for_user_create.restype = _ctypes.POINTER(sp_playlistcontainer)

def sp_session_publishedcontainer_for_user_create(session, canonical_username):
    return _sp_session_publishedcontainer_for_user_create(session, canonical_username)

_sp_session_preferred_bitrate = _libspotify.sp_session_preferred_bitrate
_sp_session_preferred_bitrate.argtypes = [_ctypes.POINTER(sp_session), sp_bitrate]
_sp_session_preferred_bitrate.restype = sp_error

@returns_sp_error
def sp_session_preferred_bitrate(session, bitrate):
    return _sp_session_preferred_bitrate(session, bitrate)

_sp_session_preferred_offline_bitrate = _libspotify.sp_session_preferred_offline_bitrate
_sp_session_preferred_offline_bitrate.argtypes = [_ctypes.POINTER(sp_session), sp_bitrate, sp_bool]
_sp_session_preferred_offline_bitrate.restype = sp_error

@returns_sp_error
def sp_session_preferred_offline_bitrate(session, bitrate, allow_resync):
    return _sp_session_preferred_offline_bitrate(session, bitrate, allow_resync)

_sp_session_get_volume_normalization = _libspotify.sp_session_get_volume_normalization
_sp_session_get_volume_normalization.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_get_volume_normalization.restype = sp_bool

def sp_session_get_volume_normalization(session):
    return (_sp_session_get_volume_normalization(session) != 0)

_sp_session_set_volume_normalization = _libspotify.sp_session_set_volume_normalization
_sp_session_set_volume_normalization.argtypes = [_ctypes.POINTER(sp_session), sp_bool]
_sp_session_set_volume_normalization.restype = sp_error

@returns_sp_error
def sp_session_set_volume_normalization(session, on):
    return _sp_session_set_volume_normalization(session, on)

_sp_session_set_private_session = _libspotify.sp_session_set_private_session
_sp_session_set_private_session.argtypes = [_ctypes.POINTER(sp_session), sp_bool]
_sp_session_set_private_session.restype = sp_error

@returns_sp_error
def sp_session_set_private_session(session, enabled):
    return _sp_session_set_private_session(session, enabled)

_sp_session_is_private_session = _libspotify.sp_session_is_private_session
_sp_session_is_private_session.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_is_private_session.restype = sp_bool

def sp_session_is_private_session(session):
    return (_sp_session_is_private_session(session) != 0)

_sp_session_set_scrobbling = _libspotify.sp_session_set_scrobbling
_sp_session_set_scrobbling.argtypes = [_ctypes.POINTER(sp_session), sp_social_provider,
                                       sp_scrobbling_state]
_sp_session_set_scrobbling.restype = sp_error

@returns_sp_error
def sp_session_set_scrobbling(session, provider, state):
    return _sp_session_set_scrobbling(session, provider, state)

_sp_session_is_scrobbling = _libspotify.sp_session_is_scrobbling
_sp_session_is_scrobbling.argtypes = [_ctypes.POINTER(sp_session), sp_social_provider,
                                      _ctypes.POINTER(sp_scrobbling_state)]
_sp_session_is_scrobbling.restype = sp_error

def sp_session_is_scrobbling(session, provider):
    state = sp_scrobbling_state()
    error = _sp_session_is_scrobbling(session, provider, _ctypes.byref(state))
    if error != SP_ERROR_OK:
        raise SpError(error)
    return state.value

_sp_session_is_scrobbling_possible = _libspotify.sp_session_is_scrobbling_possible
_sp_session_is_scrobbling_possible.argtypes = [_ctypes.POINTER(sp_session), sp_social_provider,
                                               _ctypes.POINTER(sp_bool)]
_sp_session_is_scrobbling_possible.restype = sp_error

def sp_session_is_scrobbling_possible(session, provider):
    out = sp_bool()
    error = _sp_session_is_scrobbling_possible(session, provider, _ctypes.byref(out))
    if error != SP_ERROR_OK:
        raise SpError(error)
    return (out.value != 0)

_sp_session_set_social_credentials = _libspotify.sp_session_set_social_credentials
_sp_session_set_social_credentials.argtypes = [_ctypes.POINTER(sp_session), sp_social_provider,
                                              _ctypes.c_char_p, _ctypes.c_char_p]
_sp_session_set_social_credentials.restype = sp_error

@returns_sp_error
def sp_session_set_social_credentials(session, provider, username, password):
    return _sp_session_set_social_credentials(session, provider,
            username.encode('utf-8'), password.encode('utf-8'))

_sp_session_set_connection_type = _libspotify.sp_session_set_connection_type
_sp_session_set_connection_type.argtypes = [_ctypes.POINTER(sp_session), sp_connection_type]
_sp_session_set_connection_type.restype = sp_error

@returns_sp_error
def sp_session_set_connection_type(session, conntype):
    return _sp_session_set_connection_type(session, conntype)

_sp_session_set_connection_rules = _libspotify.sp_session_set_connection_rules
_sp_session_set_connection_rules.argruless = [_ctypes.POINTER(sp_session), sp_connection_rules]
_sp_session_set_connection_rules.restype = sp_error

@returns_sp_error
def sp_session_set_connection_rules(session, rules):
    return _sp_session_set_connection_rules(session, rules)

_sp_offline_tracks_to_sync = _libspotify.sp_offline_tracks_to_sync
_sp_offline_tracks_to_sync.argtypes = [_ctypes.POINTER(sp_session)]
_sp_offline_tracks_to_sync.restype = _ctypes.c_int

def sp_offline_tracks_to_sync(session):
    return _sp_offline_tracks_to_sync(session)

_sp_offline_num_playlists = _libspotify.sp_offline_num_playlists
_sp_offline_num_playlists.argtypes = [_ctypes.POINTER(sp_session)]
_sp_offline_num_playlists.restype = _ctypes.c_int

def sp_offline_num_playlists(session):
    return _sp_offline_num_playlists(session)

_sp_offline_sync_get_status = _libspotify.sp_offline_sync_get_status
_sp_offline_sync_get_status.argtypes = [_ctypes.POINTER(sp_session),
                                        _ctypes.POINTER(sp_offline_sync_status)]
_sp_offline_sync_get_status.restype = sp_bool

def sp_offline_sync_get_status(session):
    status = sp_offline_sync_status()
    if _sp_offline_sync_get_status(session, _ctypes.byref(status)):
        return status

_sp_offline_time_left = _libspotify.sp_offline_time_left
_sp_offline_time_left.argtypes = [_ctypes.POINTER(sp_session)]
_sp_offline_time_left.restype = _ctypes.c_int

def sp_offline_time_left(session):
    return _sp_offline_time_left(session)

_sp_session_user_country = _libspotify.sp_session_user_country
_sp_session_user_country.argtypes = [_ctypes.POINTER(sp_session)]
_sp_session_user_country.restype = _ctypes.c_int

def sp_session_user_country(session):
    code = _sp_session_user_country(session)
    return  '{0}{1}'.format( chr((code & 0xFF00) >> 8),
                             chr(code & 0x00FF)        )

### Links

sp_linktype = _ctypes.c_int

SP_LINKTYPE_INVALID     = 0
SP_LINKTYPE_TRACK       = 1
SP_LINKTYPE_ALBUM       = 2
SP_LINKTYPE_ARTIST      = 3
SP_LINKTYPE_SEARCH      = 4
SP_LINKTYPE_PLAYLIST    = 5
SP_LINKTYPE_PROFILE     = 6
SP_LINKTYPE_STARRED     = 7
SP_LINKTYPE_LOCALTRACK  = 8
SP_LINKTYPE_IMAGE       = 9

_sp_link_create_from_string = _libspotify.sp_link_create_from_string
_sp_link_create_from_string.argtypes = [_ctypes.c_char_p]
_sp_link_create_from_string.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_string(link):
    return _sp_link_create_from_string(link.encode('utf-8'))

_sp_link_create_from_track = _libspotify.sp_link_create_from_track
_sp_link_create_from_track.argtypes = [_ctypes.POINTER(sp_track), _ctypes.c_int]
_sp_link_create_from_track.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_track(track, offset=0):
    return _sp_link_create_from_track(track, offset)

_sp_link_create_from_album = _libspotify.sp_link_create_from_album
_sp_link_create_from_album.argtypes = [_ctypes.POINTER(sp_album)]
_sp_link_create_from_album.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_album(album):
    return _sp_link_create_from_album(album)

_sp_link_create_from_album_cover = _libspotify.sp_link_create_from_album_cover
_sp_link_create_from_album_cover.argtypes = [_ctypes.POINTER(sp_album), sp_image_size]
_sp_link_create_from_album_cover.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_album_cover(album, size):
    return _sp_link_create_from_album_cover(album, size)

_sp_link_create_from_artist = _libspotify.sp_link_create_from_artist
_sp_link_create_from_artist.argtypes = [_ctypes.POINTER(sp_artist)]
_sp_link_create_from_artist.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_artist(artist):
    return _sp_link_create_from_artist(artist)

_sp_link_create_from_artist_portrait = _libspotify.sp_link_create_from_artist_portrait
_sp_link_create_from_artist_portrait.argtypes = [_ctypes.POINTER(sp_artist), sp_image_size]
_sp_link_create_from_artist_portrait.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_artist_portrait(artist, size):
    return _sp_link_create_from_artist_portrait(artist, size)

_sp_link_create_from_artistbrowse_portrait = _libspotify.sp_link_create_from_artistbrowse_portrait
_sp_link_create_from_artistbrowse_portrait.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_link_create_from_artistbrowse_portrait.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_artistbrowse_portrait(artistbrowse, index):
    return _sp_link_create_from_artistbrowse_portrait(artistbrowse, index)

_sp_link_create_from_search = _libspotify.sp_link_create_from_search
_sp_link_create_from_search.argtypes = [_ctypes.POINTER(sp_search)]
_sp_link_create_from_search.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_search(search):
    return _sp_link_create_from_search(search)

_sp_link_create_from_playlist = _libspotify.sp_link_create_from_playlist
_sp_link_create_from_playlist.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_link_create_from_playlist.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_playlist(playlist):
    return _sp_link_create_from_playlist(playlist)

_sp_link_create_from_user = _libspotify.sp_link_create_from_user
_sp_link_create_from_user.argtypes = [_ctypes.POINTER(sp_user)]
_sp_link_create_from_user.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_user(user):
    return _sp_link_create_from_user(user)

_sp_link_create_from_image = _libspotify.sp_link_create_from_image
_sp_link_create_from_image.argtypes = [_ctypes.POINTER(sp_image)]
_sp_link_create_from_image.restype = _ctypes.POINTER(sp_link)

def sp_link_create_from_image(image):
    return _sp_link_create_from_image(image)

_sp_link_as_string = _libspotify.sp_link_as_string
_sp_link_as_string.argtypes = [_ctypes.POINTER(sp_link), _ctypes.c_char_p, _ctypes.c_int]
_sp_link_as_string.restype = _ctypes.c_int

def sp_link_as_string(link):
    # First, we attempt to get the URI length
    buf = (_ctypes.c_char * 1)()
    link_len = _sp_link_as_string(link, buf, 1)

    buf = (_ctypes.c_char * (name_len + 1))()
    _sp_link_as_string(link, buf, link_len + 1)
    return buf.decode('utf-8')

_sp_link_type = _libspotify.sp_link_type
_sp_link_type.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_type.restype = sp_linktype

def sp_link_type(link):
    return _sp_link_type(link)

_sp_link_as_track = _libspotify.sp_link_as_track
_sp_link_as_track.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_as_track.restype = _ctypes.POINTER(sp_track)

def sp_link_as_track(link):
    return _sp_link_as_track(link)

_sp_link_as_track_and_offset = _libspotify.sp_link_as_track_and_offset
_sp_link_as_track_and_offset.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_as_track_and_offset.restype = _ctypes.POINTER(sp_track)

def sp_link_as_track_and_offset(link):
    offset = _ctypes.c_int
    track = _sp_link_as_track_and_offset(link, _ctypes.byref(offset))
    return track, offset

_sp_link_as_album = _libspotify.sp_link_as_album
_sp_link_as_album.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_as_album.restype = _ctypes.POINTER(sp_album)

def sp_link_as_album(link):
    return _sp_link_as_album(link)

_sp_link_as_artist = _libspotify.sp_link_as_artist
_sp_link_as_artist.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_as_artist.restype = _ctypes.POINTER(sp_artist)

def sp_link_as_artist(link):
    return _sp_link_as_artist(link)

_sp_link_as_user = _libspotify.sp_link_as_user
_sp_link_as_user.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_as_user.restype = _ctypes.POINTER(sp_user)

def sp_link_as_user(link):
    return _sp_link_as_user(link)

_sp_link_add_ref = _libspotify.sp_link_add_ref
_sp_link_add_ref.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_add_ref.restype = sp_error

@returns_sp_error
def sp_link_add_ref(link):
    return _sp_link_add_ref(link)

_sp_link_release = _libspotify.sp_link_release
_sp_link_release.argtypes = [_ctypes.POINTER(sp_link)]
_sp_link_release.restype = sp_error

@returns_sp_error
def sp_link_release(link):
    return _sp_link_release(link)

### Track subsystem

_sp_track_is_loaded = _libspotify.sp_track_is_loaded
_sp_track_is_loaded.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_is_loaded.restype = sp_bool

def sp_track_is_loaded(track):
    return (_sp_track_is_loaded(track) != 0)

_sp_track_error = _libspotify.sp_track_error
_sp_track_error.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_error.restype = sp_error

def sp_track_error(track):
    return _sp_track_error(track)

_sp_track_get_availability = _libspotify.sp_track_get_availability
_sp_track_get_availability.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_track_get_availability.restype = sp_track_availability

def sp_track_get_availability(session, track):
    return _sp_track_get_availability(session, track)

_sp_track_is_local = _libspotify.sp_track_is_local
_sp_track_is_local.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_track_is_local.restype = sp_bool

def sp_track_is_local(session, track):
    return (_sp_track_is_local(session, track) != 0)

_sp_track_is_autolinked = _libspotify.sp_track_is_autolinked
_sp_track_is_autolinked.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_track_is_autolinked.restype = sp_bool

def sp_track_is_autolinked(session, track):
    return (_sp_track_is_autolinked(session, track) != 0)

_sp_track_get_playable = _libspotify.sp_track_get_playable
_sp_track_get_playable.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_track_get_playable.restype = _ctypes.POINTER(sp_track)

def sp_track_get_playable(session, track):
    return _sp_track_get_playable(session, track)

_sp_track_is_placeholder = _libspotify.sp_track_is_placeholder
_sp_track_is_placeholder.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_is_placeholder.restype = sp_bool

def sp_track_is_placeholder(track):
    return (_sp_track_is_placeholder(track) != 0)

_sp_track_is_starred = _libspotify.sp_track_is_starred
_sp_track_is_starred.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_track)]
_sp_track_is_starred.restype = sp_bool

def sp_track_is_starred(session, track):
    return (_sp_track_is_starred(session, track) != 0)

_sp_track_set_starred = _libspotify.sp_track_set_starred
_sp_track_set_starred.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(_ctypes.POINTER(sp_track)),
                                 _ctypes.c_int, sp_bool]
_sp_track_set_starred.restype = sp_error

@returns_sp_error
def sp_track_set_starred(session, tracks, star):
    if star:
        c_star = 1
    else:
        c_star = 0
    tracks_array = (sp_track * len(tracks))(*tracks)
    return _sp_track_set_starred(session, tracks_array, len(tracks_array), c_star)

_sp_track_num_artists = _libspotify.sp_track_num_artists
_sp_track_num_artists.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_num_artists.restype = _ctypes.c_int

def sp_track_num_artists(track):
    return _sp_track_num_artists(track)

_sp_track_artist = _libspotify.sp_track_artist
_sp_track_artist.argtypes = [_ctypes.POINTER(sp_track), _ctypes.c_int]
_sp_track_artist.restype = _ctypes.POINTER(sp_artist)

def sp_track_artist(track, index):
    return _sp_track_artist(track, index)

_sp_track_album = _libspotify.sp_track_album
_sp_track_album.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_album.restype = _ctypes.POINTER(sp_album)

def sp_track_album(track):
    return _sp_track_album(track)

_sp_track_name = _libspotify.sp_track_name
_sp_track_name.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_name.restype = _ctypes.c_char_p

def sp_track_name(track):
    return _sp_track_name(track).decode('utf-8')

_sp_track_duration = _libspotify.sp_track_duration
_sp_track_duration.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_duration.restype = _ctypes.c_int

def sp_track_duration(track):
    return _sp_track_duration(track)

_sp_track_popularity = _libspotify.sp_track_popularity
_sp_track_popularity.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_popularity.restype = _ctypes.c_int

def sp_track_popularity(track):
    return _sp_track_popularity(track)

_sp_track_disc = _libspotify.sp_track_disc
_sp_track_disc.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_disc.restype = _ctypes.c_int

def sp_track_disc(track):
    return _sp_track_disc(track)

_sp_track_index = _libspotify.sp_track_index
_sp_track_index.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_index.restype = _ctypes.c_int

def sp_track_index(track):
    return _sp_track_index(track)

_sp_localtrack_create = _libspotify.sp_localtrack_create
_sp_localtrack_create.argtypes = [_ctypes.c_char_p, _ctypes.c_char_p, _ctypes.c_char_p, _ctypes.c_int]
_sp_localtrack_create.restype = _ctypes.POINTER(sp_track)

def sp_localtrack_create(artist, title, album, length):
    return _sp_localtrack_create(artist, title, album, length)

_sp_track_add_ref = _libspotify.sp_track_add_ref
_sp_track_add_ref.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_add_ref.restype = sp_error

@returns_sp_error
def sp_track_add_ref(track):
    return _sp_track_add_ref(track)

_sp_track_release = _libspotify.sp_track_release
_sp_track_release.argtypes = [_ctypes.POINTER(sp_track)]
_sp_track_release.restype = sp_error

@returns_sp_error
def sp_track_release(track):
    return _sp_track_release(track)

### Album subsystem

sp_albumtype = _ctypes.c_int

SP_ALBUMTYPE_ALBUM          = 0
SP_ALBUMTYPE_SINGLE         = 1
SP_ALBUMTYPE_COMPILATION    = 2
SP_ALBUMTYPE_UNKNOWN        = 3

_sp_album_is_loaded = _libspotify.sp_album_is_loaded
_sp_album_is_loaded.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_is_loaded.restype = sp_bool

def sp_album_is_loaded(album):
    return (_sp_album_is_loaded(album) != 0)

_sp_album_is_available = _libspotify.sp_album_is_available
_sp_album_is_available.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_is_available.restype = sp_bool

def sp_album_is_available(album):
    return (_sp_album_is_available(album) != 0)

_sp_album_artist = _libspotify.sp_album_artist
_sp_album_artist.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_artist.restype = _ctypes.POINTER(sp_artist)

def sp_album_artist(album):
    return _sp_album_artist(album)

_sp_album_cover = _libspotify.sp_album_cover
_sp_album_cover.argtypes = [_ctypes.POINTER(sp_album), sp_image_size]
_sp_album_cover.restype = _ctypes.POINTER(_ctypes.c_ubyte)

def sp_album_cover(album):
    return _sp_album_cover(album)

_sp_album_name = _libspotify.sp_album_name
_sp_album_name.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_name.restype = _ctypes.c_char_p

def sp_album_name(album):
    return _sp_album_name(album).decode('utf-8')

_sp_album_year = _libspotify.sp_album_year
_sp_album_year.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_year.restype = _ctypes.c_int

def sp_album_year(album):
    return _sp_album_year(album)

_sp_album_type = _libspotify.sp_album_type
_sp_album_type.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_type.restype = sp_albumtype

def sp_album_type(album):
    return _sp_album_type(album)

_sp_album_add_ref = _libspotify.sp_album_add_ref
_sp_album_add_ref.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_add_ref.restype = sp_error

@returns_sp_error
def sp_album_add_ref(album):
    return _sp_album_add_ref(album)

_sp_album_release = _libspotify.sp_album_release
_sp_album_release.argtypes = [_ctypes.POINTER(sp_album)]
_sp_album_release.restype = sp_error

@returns_sp_error
def sp_album_release(album):
    return _sp_album_release(album)

### Artist subsystem

_sp_artist_name = _libspotify.sp_artist_name
_sp_artist_name.argtypes = [_ctypes.POINTER(sp_artist)]
_sp_artist_name.restype = _ctypes.c_char_p

def sp_artist_name(artist):
    return _sp_artist_name(artist).decode('utf-8')

_sp_artist_is_loaded = _libspotify.sp_artist_is_loaded
_sp_artist_is_loaded.argtypes = [_ctypes.POINTER(sp_artist)]
_sp_artist_is_loaded.restype = sp_bool

def sp_artist_is_loaded(artist):
    return (_sp_artist_is_loaded(artist) != 0)

_sp_artist_portrait = _libspotify.sp_artist_portrait
_sp_artist_portrait.argtypes = [_ctypes.POINTER(sp_artist), sp_image_size]
_sp_artist_portrait.restype = _ctypes.POINTER(_ctypes.c_ubyte)

def sp_artist_portrait(artist):
    return _sp_artist_portrait(artist)

_sp_artist_add_ref = _libspotify.sp_artist_add_ref
_sp_artist_add_ref.argtypes = [_ctypes.POINTER(sp_artist)]
_sp_artist_add_ref.restype = sp_error

@returns_sp_error
def sp_artist_add_ref(artist):
    return _sp_artist_add_ref(artist)

_sp_artist_release = _libspotify.sp_artist_release
_sp_artist_release.argtypes = [_ctypes.POINTER(sp_artist)]
_sp_artist_release.restype = sp_error

@returns_sp_error
def sp_artist_release(artist):
    return _sp_artist_release(artist)

### Album browsing

SP_ALBUMBROWSE_COMPLETE_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_albumbrowse), _ctypes.py_object)

_sp_albumbrowse_create = _libspotify.sp_albumbrowse_create
_sp_albumbrowse_create.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_album),
                                   _ctypes.POINTER(SP_ALBUMBROWSE_COMPLETE_FUNC), _ctypes.py_object]
_sp_albumbrowse_create.restype = _ctypes.POINTER(sp_albumbrowse)

def sp_albumbrowse_create(albumbrowse, album, callback, userdata):
    return _sp_albumbrowse_create(albumbrowse, album,
            SP_ALBUMBROWSE_COMPLETE_FUNC(callback), userdata)

_sp_albumbrowse_is_loaded = _libspotify.sp_albumbrowse_is_loaded
_sp_albumbrowse_is_loaded.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_is_loaded.restype = sp_bool

def sp_albumbrowse_is_loaded(albumbrowse):
    return (_sp_albumbrowse_is_loaded(albumbrowse) != 0)

_sp_albumbrowse_error = _libspotify.sp_albumbrowse_error
_sp_albumbrowse_error.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_error.restype = sp_error

def sp_albumbrowse_error(albumbrowse):
    return _sp_albumbrowse_error(albumbrowse)

_sp_albumbrowse_album = _libspotify.sp_albumbrowse_album
_sp_albumbrowse_album.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_album.restype = _ctypes.POINTER(sp_album)

def sp_albumbrowse_album(albumbrowse):
    return _sp_albumbrowse_album(albumbrowse)

_sp_albumbrowse_artist = _libspotify.sp_albumbrowse_artist
_sp_albumbrowse_artist.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_artist.restype = _ctypes.POINTER(sp_artist)

def sp_albumbrowse_artist(albumbrowse):
    return _sp_albumbrowse_artist(albumbrowse)

_sp_albumbrowse_num_copyrights = _libspotify.sp_albumbrowse_num_copyrights
_sp_albumbrowse_num_copyrights.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_num_copyrights.restype = _ctypes.c_int

def sp_albumbrowse_num_copyrights(albumbrowse):
    return _sp_albumbrowse_num_copyrights(albumbrowse)

_sp_albumbrowse_copyright = _libspotify.sp_albumbrowse_copyright
_sp_albumbrowse_copyright.argtypes = [_ctypes.POINTER(sp_albumbrowse), _ctypes.c_int]
_sp_albumbrowse_copyright.restype = _ctypes.c_char_p

def sp_albumbrowse_copyright(albumbrowse, index):
    return _sp_albumbrowse_copyright(albumbrowse, index)

_sp_albumbrowse_num_tracks = _libspotify.sp_albumbrowse_num_tracks
_sp_albumbrowse_num_tracks.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_num_tracks.restype = _ctypes.c_int

def sp_albumbrowse_num_tracks(albumbrowse):
    return _sp_albumbrowse_num_tracks(albumbrowse)

_sp_albumbrowse_track = _libspotify.sp_albumbrowse_track
_sp_albumbrowse_track.argtypes = [_ctypes.POINTER(sp_albumbrowse), _ctypes.c_int]
_sp_albumbrowse_track.restype = _ctypes.POINTER(sp_track)

def sp_albumbrowse_track(albumbrowse, index):
    return _sp_albumbrowse_track(albumbrowse, index)

_sp_albumbrowse_review = _libspotify.sp_albumbrowse_review
_sp_albumbrowse_review.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_review.restype = _ctypes.c_char_p

def sp_albumbrowse_review(albumbrowse):
    return _sp_albumbrowse_review(albumbrowse)

_sp_albumbrowse_backend_request_duration = _libspotify.sp_albumbrowse_backend_request_duration
_sp_albumbrowse_backend_request_duration.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_backend_request_duration.restype = _ctypes.c_int

def sp_albumbrowse_backend_request_duration(albumbrowse):
    return _sp_albumbrowse_backend_request_duration(albumbrowse)

_sp_albumbrowse_add_ref = _libspotify.sp_albumbrowse_add_ref
_sp_albumbrowse_add_ref.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_add_ref.restype = sp_error

@returns_sp_error
def sp_albumbrowse_add_ref(albumbrowse):
    return _sp_albumbrowse_add_ref(albumbrowse)

_sp_albumbrowse_release = _libspotify.sp_albumbrowse_release
_sp_albumbrowse_release.argtypes = [_ctypes.POINTER(sp_albumbrowse)]
_sp_albumbrowse_release.restype = sp_error

@returns_sp_error
def sp_albumbrowse_release(albumbrowse):
    return _sp_albumbrowse_release(albumbrowse)

### Artist browsing

SP_ARTISTBROWSE_COMPLETE_FUNC = _ctypes.CFUNCTYPE(None,
    _ctypes.POINTER(sp_artistbrowse), _ctypes.py_object)

_sp_artistbrowse_create = _libspotify.sp_artistbrowse_create
_sp_artistbrowse_create.argtypes = [_ctypes.POINTER(sp_session), _ctypes.POINTER(sp_artist),
                                    sp_artistbrowse_type, _ctypes.POINTER(SP_ARTISTBROWSE_COMPLETE_FUNC),
                                    _ctypes.py_object]
_sp_artistbrowse_create.restype = _ctypes.POINTER(sp_artistbrowse)

def sp_artistbrowse_create(artistbrowse, artist, ab_type, callback, userdata):
    return _sp_artistbrowse_create(artistbrowse, artist, ab_type,
            SP_ARTISTBROWSE_COMPLETE_FUNC(callback), userdata)

_sp_artistbrowse_is_loaded = _libspotify.sp_artistbrowse_is_loaded
_sp_artistbrowse_is_loaded.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_is_loaded.restype = sp_bool

def sp_artistbrowse_is_loaded(artistbrowse):
    return (_sp_artistbrowse_is_loaded(artistbrowse) != 0)

_sp_artistbrowse_error = _libspotify.sp_artistbrowse_error
_sp_artistbrowse_error.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_error.restype = sp_error

def sp_artistbrowse_error(artistbrowse):
    return _sp_artistbrowse_error(artistbrowse)

_sp_artistbrowse_artist = _libspotify.sp_artistbrowse_artist
_sp_artistbrowse_artist.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_artist.restype = _ctypes.POINTER(sp_artist)

def sp_artistbrowse_artist(artistbrowse):
    return _sp_artistbrowse_artist(artistbrowse)

_sp_artistbrowse_num_portraits = _libspotify.sp_artistbrowse_num_portraits
_sp_artistbrowse_num_portraits.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_num_portraits.restype = _ctypes.c_int

def sp_artistbrowse_num_portraits(artistbrowse):
    return _sp_artistbrowse_num_portraits(artistbrowse)

_sp_artistbrowse_portrait = _libspotify.sp_artistbrowse_portrait
_sp_artistbrowse_portrait.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_artistbrowse_portrait.restype = _ctypes.POINTER(_ctypes.c_ubyte)

def sp_artistbrowse_portrait(artistbrowse, index):
    return _sp_artistbrowse_portrait(artistbrowse, index)

_sp_artistbrowse_num_tracks = _libspotify.sp_artistbrowse_num_tracks
_sp_artistbrowse_num_tracks.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_num_tracks.restype = _ctypes.c_int

def sp_artistbrowse_num_tracks(artistbrowse):
    return _sp_artistbrowse_num_tracks(artistbrowse)

_sp_artistbrowse_track = _libspotify.sp_artistbrowse_track
_sp_artistbrowse_track.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_artistbrowse_track.restype = _ctypes.POINTER(sp_track)

def sp_artistbrowse_track(artistbrowse, index):
    return _sp_artistbrowse_track(artistbrowse, index)

_sp_artistbrowse_num_tophit_tracks = _libspotify.sp_artistbrowse_num_tophit_tracks
_sp_artistbrowse_num_tophit_tracks.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_num_tophit_tracks.restype = _ctypes.c_int

def sp_artistbrowse_num_tophit_tracks(artistbrowse):
    return _sp_artistbrowse_num_tophit_tracks(artistbrowse)

_sp_artistbrowse_tophit_track = _libspotify.sp_artistbrowse_tophit_track
_sp_artistbrowse_tophit_track.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_artistbrowse_tophit_track.restype = _ctypes.POINTER(sp_track)

def sp_artistbrowse_tophit_track(artistbrowse, index):
    return _sp_artistbrowse_tophit_track(artistbrowse, index)

_sp_artistbrowse_num_albums = _libspotify.sp_artistbrowse_num_albums
_sp_artistbrowse_num_albums.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_num_albums.restype = _ctypes.c_int

def sp_artistbrowse_num_albums(artistbrowse):
    return _sp_artistbrowse_num_albums(artistbrowse)

_sp_artistbrowse_album = _libspotify.sp_artistbrowse_album
_sp_artistbrowse_album.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_artistbrowse_album.restype = _ctypes.POINTER(sp_album)

def sp_artistbrowse_album(artistbrowse, index):
    return _sp_artistbrowse_album(artistbrowse, index)

_sp_artistbrowse_num_similar_artists = _libspotify.sp_artistbrowse_num_similar_artists
_sp_artistbrowse_num_similar_artists.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_num_similar_artists.restype = _ctypes.c_int

def sp_artistbrowse_num_similar_artists(artistbrowse):
    return _sp_artistbrowse_num_similar_artists(artistbrowse)

_sp_artistbrowse_similar_artist = _libspotify.sp_artistbrowse_similar_artist
_sp_artistbrowse_similar_artist.argtypes = [_ctypes.POINTER(sp_artistbrowse), _ctypes.c_int]
_sp_artistbrowse_similar_artist.restype = _ctypes.POINTER(sp_artist)

def sp_artistbrowse_similar_artist(artistbrowse, index):
    return _sp_artistbrowse_similar_artist(artistbrowse, index)

_sp_artistbrowse_biography = _libspotify.sp_artistbrowse_biography
_sp_artistbrowse_biography.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_biography.restype = _ctypes.c_char_p

def sp_artistbrowse_biography(artistbrowse):
    return _sp_artistbrowse_biography(artistbrowse)

_sp_artistbrowse_backend_request_duration = _libspotify.sp_artistbrowse_backend_request_duration
_sp_artistbrowse_backend_request_duration.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_backend_request_duration.restype = _ctypes.c_int

def sp_artistbrowse_backend_request_duration(artistbrowse):
    return _sp_artistbrowse_backend_request_duration(artistbrowse)

_sp_artistbrowse_add_ref = _libspotify.sp_artistbrowse_add_ref
_sp_artistbrowse_add_ref.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_add_ref.restype = sp_error

@returns_sp_error
def sp_artistbrowse_add_ref(artistbrowse):
    return _sp_artistbrowse_add_ref(artistbrowse)

_sp_artistbrowse_release = _libspotify.sp_artistbrowse_release
_sp_artistbrowse_release.argtypes = [_ctypes.POINTER(sp_artistbrowse)]
_sp_artistbrowse_release.restype = sp_error

@returns_sp_error
def sp_artistbrowse_release(artistbrowse):
    return _sp_artistbrowse_release(artistbrowse)

# Image handling

sp_image_format = _ctypes.c_int
SP_IMAGE_FORMAT_UNKNOWN     = -1
SP_IMAGE_FORMAT_JPEG        =  0

SP_IMAGE_LOADED_CB_FUNC = _ctypes.CFUNCTYPE(None, _ctypes.POINTER(sp_image),
                                            _ctypes.c_void_p)

_sp_image_create = _libspotify.sp_image_create
_sp_image_create.argtypes = [_ctypes.POINTER(sp_session),
                             _ctypes.POINTER(_ctypes.c_byte)]
_sp_image_create.restype = _ctypes.POINTER(sp_image)

def sp_image_create(session, image_id):
    return _sp_image_create(session, image_id)

_sp_image_create_from_link = _libspotify.sp_image_create_from_link
_sp_image_create_from_link.argtypes = [_ctypes.POINTER(sp_session),
                             _ctypes.POINTER(sp_link)]
_sp_image_create_from_link.restype = _ctypes.POINTER(sp_image)

def sp_image_create_from_link(session, link):
    return _sp_image_create_from_link(session, link)

_sp_image_add_load_callback = _libspotify.sp_image_add_load_callback
_sp_image_add_load_callback.argtypes = [_ctypes.POINTER(sp_image),
        _ctypes.POINTER(SP_IMAGE_LOADED_CB_FUNC), _ctypes.py_object]
_sp_image_add_load_callback.restype = sp_error

@returns_sp_error
def sp_image_add_load_callback(image, callback, userdata):
    return _sp_image_add_load_callback(image,
            SP_IMAGE_LOADED_CB_FUNC(callback), userdata)

_sp_image_is_loaded = _libspotify.sp_image_is_loaded
_sp_image_is_loaded.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_is_loaded.restype = sp_bool

def sp_image_is_loaded(image):
    return (_sp_image_is_loaded(image) != 0)

_sp_image_error = _libspotify.sp_image_error
_sp_image_error.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_error.restype = sp_error

def sp_image_error(image):
    return _sp_image_error(image)

_sp_image_format = _libspotify.sp_image_format
_sp_image_format.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_format.restype = sp_image_format

def sp_image_format(image):
    return _sp_image_format(image)

_sp_image_data = _libspotify.sp_image_data
_sp_image_data.argtypes = [_ctypes.POINTER(sp_image), _ctypes.c_size_t]
_sp_image_data.restype = _ctypes.c_void_p

def sp_image_data(image):
    size = _ctypes.c_size_t()
    data = _sp_image_data(image, _ctypes.byref(size))
    py_data = _ctypes.create_string_buffer('', size)
    _ctypes.memmove(py_data, data, size)
    return py_data.value

_sp_image_image_id = _libspotify.sp_image_image_id
_sp_image_image_id.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_image_id.restype = _ctypes.POINTER(_ctypes.c_ubyte)

def sp_image_image_id(image):
    return _sp_image_image_id(image)

_sp_image_add_ref = _libspotify.sp_image_add_ref
_sp_image_add_ref.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_add_ref.restype = sp_error

@returns_sp_error
def sp_image_add_ref(image):
    return _sp_image_add_ref(image)

_sp_image_release = _libspotify.sp_image_release
_sp_image_release.argtypes = [_ctypes.POINTER(sp_image)]
_sp_image_release.restype = sp_error

@returns_sp_error
def sp_image_release(image):
    return _sp_image_release(image)

### Search subsystem

SP_SEARCH_COMPLETE_CB_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_search), _ctypes.py_object)

_sp_search_create = _libspotify.sp_search_create
_sp_search_create.argtypes = [_ctypes.POINTER(sp_session), _ctypes.c_char_p,
        _ctypes.c_int, _ctypes.c_int, _ctypes.c_int, _ctypes.c_int,
        _ctypes.c_int, _ctypes.c_int, _ctypes.c_int, _ctypes.c_int,
        sp_search_type, SP_SEARCH_COMPLETE_CB_FUNC, _ctypes.py_object]
_sp_search_create.restype = _ctypes.POINTER(sp_search)

def sp_search_create(session, query, track_offset, track_count, album_offset,
        album_count, artist_offset, artist_count, playlist_offset,
        playlist_count, search_type, callback, userdata):
    return _sp_search_create(session, query.encode('utf-8'), track_offset,
            track_count, album_offset, album_count, playlist_offset,
            playlist_count, search_type, SP_SEARCH_COMPLETE_CB_FUNC(callback),
            userdata)

_sp_search_is_loaded = _libspotify.sp_search_is_loaded
_sp_search_is_loaded.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_is_loaded.restype = sp_bool

def sp_search_is_loaded(search):
    return (_sp_search_is_loaded(search) != 0)

_sp_search_error = _libspotify.sp_search_error
_sp_search_error.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_error.restype = sp_error

def sp_search_error(search):
    return _sp_search_error(search)

_sp_search_num_tracks = _libspotify.sp_search_num_tracks
_sp_search_num_tracks.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_num_tracks.restype = _ctypes.c_int

def sp_search_num_tracks(search):
    return _sp_search_num_tracks(search)

_sp_search_track = _libspotify.sp_search_track
_sp_search_track.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_track.restype = _ctypes.POINTER(sp_track)

def sp_search_track(search, index):
    return _sp_search_track(search, index)

_sp_search_num_albums = _libspotify.sp_search_num_albums
_sp_search_num_albums.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_num_albums.restype = _ctypes.c_int

def sp_search_num_albums(search):
    return _sp_search_num_albums(search)

_sp_search_album = _libspotify.sp_search_album
_sp_search_album.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_album.restype = _ctypes.POINTER(sp_album)

def sp_search_album(search, index):
    return _sp_search_album(search, index)

_sp_search_num_playlists = _libspotify.sp_search_num_playlists
_sp_search_num_playlists.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_num_playlists.restype = _ctypes.c_int

def sp_search_num_playlists(search):
    return _sp_search_num_playlists(search)

_sp_search_playlist = _libspotify.sp_search_playlist
_sp_search_playlist.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_playlist.restype = _ctypes.POINTER(sp_playlist)

def sp_search_playlist(search, index):
    return _sp_search_playlist(search, index)

_sp_search_playlist_name = _libspotify.sp_search_playlist_name
_sp_search_playlist_name.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_playlist_name.restype = _ctypes.c_char_p

def sp_search_playlist_name(search, index):
    return _sp_search_playlist_name(search, index).decode('utf-8')

_sp_search_playlist_uri = _libspotify.sp_search_playlist_uri
_sp_search_playlist_uri.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_playlist_uri.restype = _ctypes.c_char_p

def sp_search_playlist_uri(search, index):
    return _sp_search_playlist_uri(search, index).decode('utf-8')

_sp_search_playlist_image_uri = _libspotify.sp_search_playlist_image_uri
_sp_search_playlist_image_uri.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_playlist_image_uri.restype = _ctypes.c_char_p

def sp_search_playlist_image_uri(search, index):
    return _sp_search_playlist_image_uri(search, index).decode('utf-8')

_sp_search_num_artists = _libspotify.sp_search_num_artists
_sp_search_num_artists.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_num_artists.restype = _ctypes.c_int

def sp_search_num_artists(search):
    return _sp_search_num_artists(search)

_sp_search_artist = _libspotify.sp_search_artist
_sp_search_artist.argtypes = [_ctypes.POINTER(sp_search), _ctypes.c_int]
_sp_search_artist.restype = _ctypes.POINTER(sp_artist)

def sp_search_artist(search, index):
    return _sp_search_artist(search, index)

_sp_search_query = _libspotify.sp_search_query
_sp_search_query.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_query.restype = _ctypes.c_char_p

def sp_search_query(search):
    return _sp_search_query(search).decode('utf-8')

_sp_search_did_you_mean = _libspotify.sp_search_did_you_mean
_sp_search_did_you_mean.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_did_you_mean.restype = _ctypes.c_char_p

def sp_search_did_you_mean(search):
    return _sp_search_did_you_mean(search).decode('utf-8')

_sp_search_total_tracks = _libspotify.sp_search_total_tracks
_sp_search_total_tracks.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_total_tracks.restype = _ctypes.c_int

def sp_search_total_tracks(search):
    return _sp_search_total_tracks(search)

_sp_search_total_albums = _libspotify.sp_search_total_albums
_sp_search_total_albums.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_total_albums.restype = _ctypes.c_int

def sp_search_total_albums(search):
    return _sp_search_total_albums(search)

_sp_search_total_artists = _libspotify.sp_search_total_artists
_sp_search_total_artists.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_total_artists.restype = _ctypes.c_int

def sp_search_total_artists(search):
    return _sp_search_total_artists(search)

_sp_search_total_playlists = _libspotify.sp_search_total_playlists
_sp_search_total_playlists.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_total_playlists.restype = _ctypes.c_int

def sp_search_total_playlists(search):
    return _sp_search_total_playlists(search)

_sp_search_add_ref = _libspotify.sp_search_add_ref
_sp_search_add_ref.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_add_ref.restype = sp_error

@returns_sp_error
def sp_search_add_ref(search):
    return _sp_search_add_ref(search)

_sp_search_release = _libspotify.sp_search_release
_sp_search_release.argtypes = [_ctypes.POINTER(sp_search)]
_sp_search_release.restype = sp_error

@returns_sp_error
def sp_search_release(search):
    return _sp_search_release(search)
