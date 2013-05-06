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

sp_playlist_type = _ctypes.c_int

SP_PLAYLIST_TYPE_PLAYLIST = 0
SP_PLAYLIST_TYPE_START_FOLDER = 1
SP_PLAYLIST_TYPE_END_FOLDER = 2
SP_PLAYLIST_TYPE_PLACEHOLDER = 3

sp_search_type = _ctypes.c_int

SP_SEARCH_STANDARD = 0
SP_SEARCH_SUGGEST = 1

sp_playlist_offline_status = _ctypes.c_int

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

### Playlist subsystem

SP_PLAYLIST_TRACKS_ADDED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(_ctypes.POINTER(sp_track)), _ctypes.c_int,
        _ctypes.c_int, _ctypes.py_object)

SP_PLAYLIST_TRACKS_REMOVED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.POINTER(_ctypes.c_int),
        _ctypes.c_int, _ctypes.py_object)

SP_PLAYLIST_TRACKS_MOVED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.POINTER(_ctypes.c_int),
        _ctypes.c_int, _ctypes.c_int, _ctypes.py_object)

SP_PLAYLIST_PLAYLIST_RENAMED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.py_object)

SP_PLAYLIST_PLAYLIST_STATE_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.py_object)

SP_PLAYLIST_PLAYLIST_UPDATE_IN_PROGRESS_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), sp_bool, _ctypes.py_object)

SP_PLAYLIST_PLAYLIST_METADATA_UPDATED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.py_object)

SP_PLAYLIST_TRACK_CREATED_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.c_int, _ctypes.POINTER(sp_user),
        _ctypes.c_int, _ctypes.py_object)

SP_PLAYLIST_TRACK_SEEN_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.c_int, sp_bool,
        _ctypes.py_object)

SP_PLAYLIST_DESCRIPTION_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.c_char_p, _ctypes.py_object)

SP_PLAYLIST_IMAGE_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.POINTER(_ctypes.c_ubyte),
        _ctypes.py_object)

SP_PLAYLIST_TRACK_MESSAGE_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.c_int, _ctypes.c_char_p,
        _ctypes.py_object)

SP_PLAYLIST_SUBSCRIBERS_CHANGED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlist), _ctypes.py_object)

class sp_playlist_callbacks(_ctypes.Structure):
    _fields_ = [
        ('tracks_added', SP_PLAYLIST_TRACKS_ADDED_FUNC),
        ('tracks_removed', SP_PLAYLIST_TRACKS_REMOVED_FUNC),
        ('tracks_moved', SP_PLAYLIST_TRACKS_MOVED_FUNC),
        ('playlist_renamed', SP_PLAYLIST_PLAYLIST_RENAMED_FUNC),
        ('playlist_state_changed', SP_PLAYLIST_PLAYLIST_STATE_CHANGED_FUNC),
        ('playlist_update_in_progress',
            SP_PLAYLIST_PLAYLIST_UPDATE_IN_PROGRESS_FUNC),
        ('playlist_metadata_updated',
            SP_PLAYLIST_PLAYLIST_METADATA_UPDATED_FUNC),
        ('track_created_changed', SP_PLAYLIST_TRACK_CREATED_CHANGED_FUNC),
        ('track_seen_changed', SP_PLAYLIST_TRACK_SEEN_CHANGED_FUNC),
        ('description_changed', SP_PLAYLIST_DESCRIPTION_CHANGED_FUNC),
        ('image_changed', SP_PLAYLIST_IMAGE_CHANGED_FUNC),
        ('track_message_changed', SP_PLAYLIST_TRACK_MESSAGE_CHANGED_FUNC),
        ('subscribers_changed', SP_PLAYLIST_SUBSCRIBERS_CHANGED_FUNC),
    ]

_sp_playlist_is_loaded = _libspotify.sp_playlist_is_loaded
_sp_playlist_is_loaded.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_is_loaded.restype = sp_bool

def sp_playlist_is_loaded(playlist):
    return (_sp_playlist_is_loaded(playlist) != 0)

_sp_playlist_add_callbacks = _libspotify.sp_playlist_add_callbacks
_sp_playlist_add_callbacks.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(sp_playlist_callbacks), _ctypes.py_object]
_sp_playlist_add_callbacks.restype = sp_error

@returns_sp_error
def sp_playlist_add_callbacks(playlist, callbacks, userdata):
    return _sp_playlist_add_callbacks(playlist, callbacks, userdata)

_sp_playlist_remove_callbacks = _libspotify.sp_playlist_remove_callbacks
_sp_playlist_remove_callbacks.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(sp_playlist_callbacks), _ctypes.py_object]
_sp_playlist_remove_callbacks.restype = sp_error

@returns_sp_error
def sp_playlist_remove_callbacks(playlist, callbacks, userdata):
    return _sp_playlist_remove_callbacks(playlist, callbacks, userdata)

_sp_playlist_num_tracks = _libspotify.sp_playlist_num_tracks
_sp_playlist_num_tracks.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_num_tracks.restype = _ctypes.c_int

def sp_playlist_num_tracks(playlist):
    return _sp_playlist_num_tracks(playlist)

_sp_playlist_track = _libspotify.sp_playlist_track
_sp_playlist_track.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_int]
_sp_playlist_track.restype = _ctypes.POINTER(sp_track)

def sp_playlist_track(playlist, index):
    return _sp_playlist_track(playlist, index)

_sp_playlist_track_create_time = _libspotify.sp_playlist_track_create_time
_sp_playlist_track_create_time.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_int]
_sp_playlist_track_create_time.restype = _ctypes.c_int

def sp_playlist_track_create_time(playlist, index):
    return _sp_playlist_track_create_time(playlist, index)

_sp_playlist_track_creator = _libspotify.sp_playlist_track_creator
_sp_playlist_track_creator.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_int]
_sp_playlist_track_creator.restype = _ctypes.POINTER(sp_user)

def sp_playlist_track_creator(playlist, index):
    return _sp_playlist_track_creator(playlist, index)

_sp_playlist_track_seen = _libspotify.sp_playlist_track_seen
_sp_playlist_track_seen.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_int]
_sp_playlist_track_seen.restype = sp_bool

def sp_playlist_track_seen(playlist, index):
    return (_sp_playlist_track_seen(playlist, index) != 0)

_sp_playlist_track_set_seen = _libspotify.sp_playlist_track_set_seen
_sp_playlist_track_set_seen.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.c_int, sp_bool]
_sp_playlist_track_set_seen.restype = sp_error

@returns_sp_error
def sp_playlist_track_set_seen(playlist, index, seen):
    return _sp_playlist_track_set_seen(playlist, index, seen)

_sp_playlist_track_message = _libspotify.sp_playlist_track_message
_sp_playlist_track_message.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_int]
_sp_playlist_track_message.restype = _ctypes.c_char_p

def sp_playlist_track_message(playlist, index):
    message = _sp_playlist_track_message(playlist, index)
    if message is not None:
        return message.decode('utf-8')

_sp_playlist_name = _libspotify.sp_playlist_name
_sp_playlist_name.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_name.restype = _ctypes.c_char_p

def sp_playlist_name(playlist):
    return _sp_playlist_name(playlist).decode('utf-8')

_sp_playlist_rename = _libspotify.sp_playlist_rename
_sp_playlist_rename.argtypes = [_ctypes.POINTER(sp_playlist), _ctypes.c_char_p]
_sp_playlist_rename.restype = sp_error

@returns_sp_error
def sp_playlist_rename(playlist, new_name):
    return _sp_playlist_rename(playlist, new_name)

_sp_playlist_owner = _libspotify.sp_playlist_owner
_sp_playlist_owner.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_owner.restype = _ctypes.POINTER(sp_user)

def sp_playlist_owner(playlist):
    return _sp_playlist_owner(playlist)

_sp_playlist_is_collaborative = _libspotify.sp_playlist_is_collaborative
_sp_playlist_is_collaborative.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_is_collaborative.restype = sp_bool

def sp_playlist_is_collaborative(playlist):
    return (_sp_playlist_is_collaborative(playlist) != 0)

_sp_playlist_set_collaborative = _libspotify.sp_playlist_set_collaborative
_sp_playlist_set_collaborative.argtypes = [_ctypes.POINTER(sp_playlist),
        sp_bool]
_sp_playlist_set_collaborative.restype = sp_error

@returns_sp_error
def sp_playlist_set_collaborative(playlist, collaborative):
    return _sp_playlist_set_collaborative(playlist, collaborative)

_sp_playlist_set_autolink_tracks = _libspotify.sp_playlist_set_autolink_tracks
_sp_playlist_set_autolink_tracks.argtypes = [_ctypes.POINTER(sp_playlist),
        sp_bool]
_sp_playlist_set_autolink_tracks.restype = sp_error

@returns_sp_error
def sp_playlist_set_autolink_tracks(playlist, link):
    return _sp_playlist_set_autolink_tracks(playlist, link)

_sp_playlist_get_description = _libspotify.sp_playlist_get_description
_sp_playlist_get_description.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_get_description.restype = _ctypes.c_char_p

def sp_playlist_get_description(playlist):
    description = _sp_playlist_get_description(playlist)
    if description is not None:
        return description.decode('utf-8')

_sp_playlist_get_image = _libspotify.sp_playlist_get_image
_sp_playlist_get_image.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(_ctypes.c_ubyte)]
_sp_playlist_get_image.restype = sp_bool

def sp_playlist_get_image(playlist):
    image = (_ctypes.c_ubyte * 20)()
    has_image = _sp_playlist_get_image(playlist, image)
    if has_image:
        return image

_sp_playlist_has_pending_changes = _libspotify.sp_playlist_has_pending_changes
_sp_playlist_has_pending_changes.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_has_pending_changes.restype = sp_bool

def sp_playlist_has_pending_changes(playlist):
    return (_sp_playlist_has_pending_changes(playlist) != 0)

_sp_playlist_add_tracks = _libspotify.sp_playlist_add_tracks
_sp_playlist_add_tracks.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(_ctypes.POINTER(sp_track)), _ctypes.c_int,
        _ctypes.c_int, _ctypes.POINTER(sp_session)]
_sp_playlist_add_tracks.restype = sp_error

@returns_sp_error
def sp_playlist_add_tracks(playlist, tracks, position, session):
    tracks_array = (_ctypes.POINTER(sp_track) * len(tracks))(*tracks)
    return _sp_playlist_add_tracks(playlist, tracks_array, len(tracks),
            position, session)

_sp_playlist_remove_tracks = _libspotify.sp_playlist_remove_tracks
_sp_playlist_remove_tracks.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(_ctypes.c_int), _ctypes.c_int]
_sp_playlist_remove_tracks.restype = sp_error

@returns_sp_error
def sp_playlist_remove_tracks(playlist, tracks):
    tracks_array = (_ctypes.c_int * len(tracks))(*tracks)
    return _sp_playlist_remove_tracks(playlist, tracks_array, len(tracks))

_sp_playlist_reorder_tracks = _libspotify.sp_playlist_reorder_tracks
_sp_playlist_reorder_tracks.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(_ctypes.c_int), _ctypes.c_int, _ctypes.c_int]
_sp_playlist_reorder_tracks.restype = sp_error

@returns_sp_error
def sp_playlist_reorder_tracks(playlist, tracks, new_position):
    tracks_array = (_ctypes.c_int * len(tracks))(*tracks)
    return _sp_playlist_reorder_tracks(playlist, tracks_array, len(tracks),
            new_position)

_sp_playlist_num_subscribers = _libspotify.sp_playlist_num_subscribers
_sp_playlist_num_subscribers.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_num_subscribers.restype = _ctypes.c_uint

def sp_playlist_num_subscribers(playlist):
    return _sp_playlist_num_subscribers(playlist)

_sp_playlist_subscribers = _libspotify.sp_playlist_subscribers
_sp_playlist_subscribers.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_subscribers.restype = _ctypes.POINTER(sp_subscribers)

_sp_playlist_subscribers_free = _libspotify.sp_playlist_subscribers_free
_sp_playlist_subscribers_free.argtypes = [_ctypes.POINTER(sp_subscribers)]
_sp_playlist_subscribers_free.restype = sp_error

def sp_playlist_subscribers(playlist):
    subscribers_struct = _sp_playlist_subscribers(playlist)
    subscribers = [subscribers_struct.subscribers[i].value.decode('utf-8')
                        for i in range(subscribers_struct.count.value)]
    _sp_playlist_subscribers_free(subscribers_struct)
    return subscribers

_sp_playlist_update_subscribers = _libspotify.sp_playlist_update_subscribers
_sp_playlist_update_subscribers.argtypes = [_ctypes.POINTER(sp_playlist),
        _ctypes.POINTER(sp_session)]
_sp_playlist_update_subscribers.restype = sp_error

@returns_sp_error
def sp_playlist_update_subscribers(playlist, session):
    return _sp_playlist_update_subscribers(playlist, session)

_sp_playlist_is_in_ram = _libspotify.sp_playlist_is_in_ram
_sp_playlist_is_in_ram.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_playlist)]
_sp_playlist_is_in_ram.restype = sp_bool

def sp_playlist_is_in_ram(session, playlist):
    return (_sp_playlist_is_in_ram(session, playlist) != 0)

_sp_playlist_set_in_ram = _libspotify.sp_playlist_set_in_ram
_sp_playlist_set_in_ram.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_playlist), sp_bool]
_sp_playlist_set_in_ram.restype = sp_error

@returns_sp_error
def sp_playlist_set_in_ram(session, playlist, in_ram):
    return _sp_playlist_set_in_ram(session, playlist, in_ram)

_sp_playlist_create = _libspotify.sp_playlist_create
_sp_playlist_create.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_link)]
_sp_playlist_create.restype = _ctypes.POINTER(sp_playlist)

def sp_playlist_create(session, link):
    return _sp_playlist_create(session, link)

_sp_playlist_set_offline_mode = _libspotify.sp_playlist_set_offline_mode
_sp_playlist_set_offline_mode.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_playlist), sp_bool]
_sp_playlist_set_offline_mode.restype = sp_error

@returns_sp_error
def sp_playlist_set_offline_mode(session, playlist, offline):
    return _sp_playlist_set_offline_mode(session, playlist, offline)

_sp_playlist_get_offline_status = _libspotify.sp_playlist_get_offline_status
_sp_playlist_get_offline_status.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_playlist)]
_sp_playlist_get_offline_status.restype = sp_playlist_offline_status

def sp_playlist_get_offline_status(session, playlist):
    return _sp_playlist_get_offline_status(session, playlist)

_sp_playlist_get_offline_download_completed = _libspotify.sp_playlist_get_offline_download_completed
_sp_playlist_get_offline_download_completed.argtypes = [_ctypes.POINTER(sp_session),
        _ctypes.POINTER(sp_playlist)]
_sp_playlist_get_offline_download_completed.restype = _ctypes.c_int

def sp_playlist_get_offline_download_completed(session, playlist):
    return _sp_playlist_get_offline_download_completed(session, playlist)

_sp_playlist_add_ref = _libspotify.sp_playlist_add_ref
_sp_playlist_add_ref.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_add_ref.restype = sp_error

@returns_sp_error
def sp_playlist_add_ref(playlist):
    return _sp_playlist_add_ref(playlist)

_sp_playlist_release = _libspotify.sp_playlist_release
_sp_playlist_release.argtypes = [_ctypes.POINTER(sp_playlist)]
_sp_playlist_release.restype = sp_error

@returns_sp_error
def sp_playlist_release(playlist):
    return _sp_playlist_release(playlist)

### Playlist containers

SP_PLAYLISTCONTAINER_PLAYLIST_ADDED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_playlist),
        _ctypes.c_int, _ctypes.py_object)

SP_PLAYLISTCONTAINER_PLAYLIST_REMOVED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_playlist),
        _ctypes.c_int, _ctypes.py_object)

SP_PLAYLISTCONTAINER_PLAYLIST_MOVED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_playlist),
        _ctypes.c_int, _ctypes.c_int, _ctypes.py_object)

SP_PLAYLISTCONTAINER_CONTAINER_LOADED_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_playlistcontainer), _ctypes.py_object)

class sp_playlistcontainer_callbacks(_ctypes.Structure):
    _fields_ = [
        ('playlist_added', SP_PLAYLISTCONTAINER_PLAYLIST_ADDED_FUNC),
        ('playlist_removed', SP_PLAYLISTCONTAINER_PLAYLIST_REMOVED_FUNC),
        ('playlist_moved', SP_PLAYLISTCONTAINER_PLAYLIST_MOVED_FUNC),
        ('container_loaded', SP_PLAYLISTCONTAINER_CONTAINER_LOADED_FUNC),
    ]

_sp_playlistcontainer_add_callbacks = \
        _libspotify.sp_playlistcontainer_add_callbacks
_sp_playlistcontainer_add_callbacks.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer),
        _ctypes.POINTER(sp_playlistcontainer_callbacks), _ctypes.py_object]
_sp_playlistcontainer_add_callbacks.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_add_callbacks(container, callbacks, userdata):
    return _sp_playlistcontainer_add_callbacks(container, callbacks,
            userdata)

_sp_playlistcontainer_remove_callbacks = \
        _libspotify.sp_playlistcontainer_remove_callbacks
_sp_playlistcontainer_remove_callbacks.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer),
        _ctypes.POINTER(sp_playlistcontainer_callbacks), _ctypes.py_object]
_sp_playlistcontainer_remove_callbacks.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_remove_callbacks(container, callbacks,
        userdata):
    return _sp_playlistcontainer_remove_callbacks(container, callbacks,
            userdata)

_sp_playlistcontainer_num_playlists = \
        _libspotify.sp_playlistcontainer_num_playlists
_sp_playlistcontainer_num_playlists.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer)]
_sp_playlistcontainer_num_playlists.restype = _ctypes.c_int

def sp_playlistcontainer_num_playlists(playlistcontainer):
    return _sp_playlistcontainer_num_playlists(playlistcontainer)

_sp_playlistcontainer_is_loaded = _libspotify.sp_playlistcontainer_is_loaded
_sp_playlistcontainer_is_loaded.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer)]
_sp_playlistcontainer_is_loaded.restype = sp_bool

def sp_playlistcontainer_is_loaded(playlistcontainer):
    return (_sp_playlistcontainer_is_loaded(playlistcontainer) != 0)

_sp_playlistcontainer_playlist = _libspotify.sp_playlistcontainer_playlist
_sp_playlistcontainer_playlist.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int]
_sp_playlistcontainer_playlist.restype = _ctypes.POINTER(sp_playlist)

def sp_playlistcontainer_playlist(container, index):
    return _sp_playlistcontainer_playlist(container, index)

_sp_playlistcontainer_playlist_type = \
        _libspotify.sp_playlistcontainer_playlist_type
_sp_playlistcontainer_playlist_type.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int]
_sp_playlistcontainer_playlist_type.restype = sp_playlist_type

def sp_playlistcontainer_playlist_type(container, index):
    return _sp_playlistcontainer_playlist_type(container, index)

_sp_playlistcontainer_playlist_folder_name = \
        _libspotify.sp_playlistcontainer_playlist_folder_name
_sp_playlistcontainer_playlist_folder_name.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int,
                _ctypes.c_char_p, _ctypes.c_int]
_sp_playlistcontainer_playlist_folder_name.restype = sp_error

def sp_playlistcontainer_playlist_folder_name(container, index):
    buf = _ctypes.create_string_buffer(256)
    err = _sp_playlistcontainer_playlist_folder_name(container, index,
            buf, 256)
    if err != SP_ERROR_OK:
        raise SpError(err)
    return buf.value.decode('utf-8')

_sp_playlistcontainer_playlist_folder_id = \
        _libspotify.sp_playlistcontainer_playlist_folder_id
_sp_playlistcontainer_playlist_folder_id.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int]
_sp_playlistcontainer_playlist_folder_id.restype = _ctypes.c_uint64

def sp_playlistcontainer_playlist_folder_id(container, index):
    return _sp_playlistcontainer_playlist_folder_id(container, index)

_sp_playlistcontainer_add_new_playlist = \
        _libspotify.sp_playlistcontainer_add_new_playlist
_sp_playlistcontainer_add_new_playlist.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_char_p]
_sp_playlistcontainer_add_new_playlist.restype = _ctypes.POINTER(sp_playlist)

def sp_playlistcontainer_add_new_playlist(container, name):
    return _sp_playlistcontainer_add_new_playlist(container,
            name.encode('utf-8'))

_sp_playlistcontainer_add_playlist = \
        _libspotify.sp_playlistcontainer_add_playlist
_sp_playlistcontainer_add_playlist.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_link)]
_sp_playlistcontainer_add_playlist.restype = _ctypes.POINTER(sp_playlist)

def sp_playlistcontainer_add_playlist(container, link):
    return _sp_playlistcontainer_add_playlist(container, link)

_sp_playlistcontainer_remove_playlist = \
        _libspotify.sp_playlistcontainer_remove_playlist
_sp_playlistcontainer_remove_playlist.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int]
_sp_playlistcontainer_remove_playlist.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_remove_playlist(container, index):
    return _sp_playlistcontainer_remove_playlist(container, index)

_sp_playlistcontainer_move_playlist = \
        _libspotify.sp_playlistcontainer_move_playlist
_sp_playlistcontainer_move_playlist.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int, _ctypes.c_int,
                sp_bool]
_sp_playlistcontainer_move_playlist.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_move_playlist(container, index, new_position, dry_run):
    return _sp_playlistcontainer_move_playlist(container, index, new_position,
            dry_run)

_sp_playlistcontainer_add_folder = \
        _libspotify.sp_playlistcontainer_add_folder
_sp_playlistcontainer_add_folder.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.c_int, _ctypes.c_char_p]
_sp_playlistcontainer_add_folder.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_add_folder(container, index, name):
    return _sp_playlistcontainer_add_folder(container, index,
            name.encode('utf-8'))

_sp_playlistcontainer_owner = _libspotify.sp_playlistcontainer_owner
_sp_playlistcontainer_owner.argtypes = [_ctypes.POINTER(sp_playlistcontainer)]
_sp_playlistcontainer_owner.restype = _ctypes.POINTER(sp_user)

def sp_playlistcontainer_owner(container):
    return _sp_playlistcontainer_owner(container)

_sp_playlistcontainer_add_ref = _libspotify.sp_playlistcontainer_add_ref
_sp_playlistcontainer_add_ref.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer)]
_sp_playlistcontainer_add_ref.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_add_ref(playlistcontainer):
    return _sp_playlistcontainer_add_ref(playlistcontainer)

_sp_playlistcontainer_release = _libspotify.sp_playlistcontainer_release
_sp_playlistcontainer_release.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer)]
_sp_playlistcontainer_release.restype = sp_error

@returns_sp_error
def sp_playlistcontainer_release(playlistcontainer):
    return _sp_playlistcontainer_release(playlistcontainer)

_sp_playlistcontainer_get_unseen_tracks = \
        _libspotify.sp_playlistcontainer_get_unseen_tracks
_sp_playlistcontainer_get_unseen_tracks.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_playlist),
                _ctypes.POINTER(_ctypes.POINTER(sp_track)), _ctypes.c_int]
_sp_playlistcontainer_get_unseen_tracks.restype = _ctypes.c_int

def sp_playlistcontainer_get_unseen_tracks(container, playlist):
    # First, we get the number of unseen tracks
    num_tracks = _sp_playlistcontainer_get_unseen_tracks(container, playlist,
            None, 0)
    if num_tracks < 0:
        return None # Error
    elif num_tracks == 0:
        return []

    tracks_array = (_ctypes.POINTER(sp_track) * num_tracks)()
    _sp_playlistcontainer_get_unseen_tracks(container, playlist, tracks_array,
            num_tracks)
    return [tracks_array[i].value for i in range(num_tracks)]

_sp_playlistcontainer_clear_unseen_tracks = \
        _libspotify.sp_playlistcontainer_clear_unseen_tracks
_sp_playlistcontainer_clear_unseen_tracks.argtypes = \
        [_ctypes.POINTER(sp_playlistcontainer), _ctypes.POINTER(sp_playlist)]
_sp_playlistcontainer_clear_unseen_tracks.restype = _ctypes.c_int

def sp_playlistcontainer_clear_unseen_tracks(container, playlist):
    return _sp_playlistcontainer_clear_unseen_tracks(container, playlist)

### User handling

sp_relation_type = _ctypes.c_int

SP_RELATION_TYPE_UNKNOWN        = 0
SP_RELATION_TYPE_NONE           = 1
SP_RELATION_TYPE_UNIDIRECTIONAL = 2
SP_RELATION_TYPE_BIDIRECTIONAL  = 3

_sp_user_canonical_name = _libspotify.sp_user_canonical_name
_sp_user_canonical_name.argtypes = [_ctypes.POINTER(sp_user)]
_sp_user_canonical_name.restype = _ctypes.c_char_p

def sp_user_canonical_name(user):
    return _sp_user_canonical_name(user).decode('utf-8')

_sp_user_display_name = _libspotify.sp_user_display_name
_sp_user_display_name.argtypes = [_ctypes.POINTER(sp_user)]
_sp_user_display_name.restype = _ctypes.c_char_p

def sp_user_display_name(user):
    return _sp_user_display_name(user).decode('utf-8')

_sp_user_is_loaded = _libspotify.sp_user_is_loaded
_sp_user_is_loaded.argtypes = [_ctypes.POINTER(sp_user)]
_sp_user_is_loaded.restype = sp_bool

def sp_user_is_loaded(user):
    return (_sp_user_is_loaded(user) != 0)

_sp_user_add_ref = _libspotify.sp_user_add_ref
_sp_user_add_ref.argtypes = [_ctypes.POINTER(sp_user)]
_sp_user_add_ref.restype = sp_error

@returns_sp_error
def sp_user_add_ref(user):
    return _sp_user_add_ref(user)

_sp_user_release = _libspotify.sp_user_release
_sp_user_release.argtypes = [_ctypes.POINTER(sp_user)]
_sp_user_release.restype = sp_error

@returns_sp_error
def sp_user_release(user):
    return _sp_user_release(user)

### Toplist handling

sp_toplisttype = _ctypes.c_int

SP_TOPLIST_TYPE_ARTISTS = 0
SP_TOPLIST_TYPE_ALBUMS  = 1
SP_TOPLIST_TYPE_TRACKS  = 2

sp_toplistregion = _ctypes.c_int

# we want 'everywhere' and 'user' for these
_SP_TOPLIST_REGION_EVERYWHERE = 0
_SP_TOPLIST_REGION_USER       = 1

def _str_to_toplistregion(region):
    if region == 'everywhere':
        return _SP_TOPLIST_REGION_EVERYWHERE
    if region == 'user':
        return _SP_TOPLIST_REGION_USER
    return (ord(region[0]) << 8) | ord(region[1])

SP_TOPLISTBROWSE_COMPLETE_FUNC = _ctypes.CFUNCTYPE(None,
        _ctypes.POINTER(sp_toplistbrowse), _ctypes.py_object)

_sp_toplistbrowse_create = _libspotify.sp_toplistbrowse_create
_sp_toplistbrowse_create.argtypes = [_ctypes.POINTER(sp_session),
        sp_toplisttype, sp_toplistregion, _ctypes.c_char_p,
        SP_TOPLISTBROWSE_COMPLETE_FUNC, _ctypes.py_object]
_sp_toplistbrowse_create.restype = _ctypes.POINTER(sp_toplistbrowse)

def sp_toplistbrowse_create(toplistbrowse, type, region, username, callback,
        userdata):
    c_username = None
    if username is not None:
        c_username = username.encode('utf-8')

    return _sp_toplistbrowse_create(toplistbrowse, type,
            _str_to_toplistregion(region), c_username,
            SP_TOPLISTBROWSE_COMPLETE_FUNC(callback), userdata)

_sp_toplistbrowse_is_loaded = _libspotify.sp_toplistbrowse_is_loaded
_sp_toplistbrowse_is_loaded.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_is_loaded.restype = sp_bool

def sp_toplistbrowse_is_loaded(toplistbrowse):
    return (_sp_toplistbrowse_is_loaded(toplistbrowse) != 0)

_sp_toplistbrowse_error = _libspotify.sp_toplistbrowse_error
_sp_toplistbrowse_error.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_error.restype = sp_error

def sp_toplistbrowse_error(toplistbrowse):
    return _sp_toplistbrowse_error(toplistbrowse)

_sp_toplistbrowse_add_ref = _libspotify.sp_toplistbrowse_add_ref
_sp_toplistbrowse_add_ref.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_add_ref.restype = sp_error

@returns_sp_error
def sp_toplistbrowse_add_ref(toplistbrowse):
    return _sp_toplistbrowse_add_ref(toplistbrowse)

_sp_toplistbrowse_release = _libspotify.sp_toplistbrowse_release
_sp_toplistbrowse_release.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_release.restype = sp_error

@returns_sp_error
def sp_toplistbrowse_release(toplistbrowse):
    return _sp_toplistbrowse_release(toplistbrowse)

_sp_toplistbrowse_num_artists = _libspotify.sp_toplistbrowse_num_artists
_sp_toplistbrowse_num_artists.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_num_artists.restype = _ctypes.c_int

def sp_toplistbrowse_num_artists(toplistbrowse):
    return _sp_toplistbrowse_num_artists(toplistbrowse)

_sp_toplistbrowse_artist = _libspotify.sp_toplistbrowse_artist
_sp_toplistbrowse_artist.argtypes = [_ctypes.POINTER(sp_toplistbrowse), _ctypes.c_int]
_sp_toplistbrowse_artist.restype = _ctypes.POINTER(sp_artist)

def sp_toplistbrowse_artist(toplistbrowse, index):
    return _sp_toplistbrowse_artist(toplistbrowse, index)

_sp_toplistbrowse_num_albums = _libspotify.sp_toplistbrowse_num_albums
_sp_toplistbrowse_num_albums.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_num_albums.restype = _ctypes.c_int

def sp_toplistbrowse_num_albums(toplistbrowse):
    return _sp_toplistbrowse_num_albums(toplistbrowse)

_sp_toplistbrowse_album = _libspotify.sp_toplistbrowse_album
_sp_toplistbrowse_album.argtypes = [_ctypes.POINTER(sp_toplistbrowse), _ctypes.c_int]
_sp_toplistbrowse_album.restype = _ctypes.POINTER(sp_album)

def sp_toplistbrowse_album(toplistbrowse, index):
    return _sp_toplistbrowse_album(toplistbrowse, index)

_sp_toplistbrowse_num_tracks = _libspotify.sp_toplistbrowse_num_tracks
_sp_toplistbrowse_num_tracks.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_num_tracks.restype = _ctypes.c_int

def sp_toplistbrowse_num_tracks(toplistbrowse):
    return _sp_toplistbrowse_num_tracks(toplistbrowse)

_sp_toplistbrowse_track = _libspotify.sp_toplistbrowse_track
_sp_toplistbrowse_track.argtypes = [_ctypes.POINTER(sp_toplistbrowse), _ctypes.c_int]
_sp_toplistbrowse_track.restype = _ctypes.POINTER(sp_track)

def sp_toplistbrowse_track(toplistbrowse, index):
    return _sp_toplistbrowse_track(toplistbrowse, index)

_sp_toplistbrowse_backend_request_duration = _libspotify.sp_toplistbrowse_backend_request_duration
_sp_toplistbrowse_backend_request_duration.argtypes = [_ctypes.POINTER(sp_toplistbrowse)]
_sp_toplistbrowse_backend_request_duration.restype = _ctypes.c_int

def sp_toplistbrowse_backend_request_duration(toplistbrowse):
    return _sp_toplistbrowse_backend_request_duration(toplistbrowse)
