# Mock artist

from spotify import capi
from spotify.mock import MockSpotifyObject

class Artist(MockSpotifyObject):

    _prefix = 'artist'

    def __init__(self, name='', portrait=None, is_loaded=False):
        MockSpotifyObject.__init__(self, name, portrait, is_loaded)
