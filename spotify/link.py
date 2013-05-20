# -*- coding: utf-8 -*-

from spotify import capi
from spotify.generic import SpotifyObject

class Link(SpotifyObject):

    _prefix = 'link'

    @classmethod
    def from_uri(cls, uri):
        c_link = capi.sp_link_create_from_string(uri)
        if not c_link:
            raise ValueError("Unable to parse uri")
        return cls._from_cdata(c_link, add_ref=False)
