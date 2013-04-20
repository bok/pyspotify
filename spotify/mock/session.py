# Mock session

from spotify import capi
from spotify.mock import MockSpotifyObject

class Session(MockSpotifyObject):

    _prefix = 'session'

    def __init__(self,
                 config = None,
                 connection_state = capi.SP_CONNECTION_STATE_LOGGED_OUT,
                 offline_time_left = 0,
                 offline_sync_status = None,
                 offline_num_playlists = 0,
                 offline_tracks_to_sync = 0,
                 inbox = None, user = None,
                 scrobbling_possible  = 0):
        MockSpotifyObject.__init__(self, config, connection_state,
                                   offline_time_left, offline_sync_status,
                                   offline_num_playlists,
                                   offline_tracks_to_sync, inbox, user,
                                   scrobbling_possible)
