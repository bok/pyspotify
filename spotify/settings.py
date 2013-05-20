# -*- coding: utf-8 -*-
#
# Settings for session creation

class Settings(object):
    """
    This class stores settings used when creating a Spotify session.
    """

    application_key = None
    """
    Your application key (binary string).
    """

    ca_certs_filename = None
    """
    Path to a file containing the root ca certificates that the peer should be
    verified with. The file must be a concatenation of all certificates in PEM
    format. Provided with libspotify is a sample pem file in examples. It is
    recommended that the application export a similar file from the local
    certificate store.
    """

    cache_location = 'tmp'
    """
    The location where Spotify will write cache files. This cache include
    tracks, cached browse results and coverarts. Set to ``''`` to disable
    cache.
    """

    compress_playlists = False
    """
    Compress local copy of playlists, reduces disk space usage.
    """

    device_id = None
    """
    Device ID for offline synchronization and logging purposes. The Device Id
    must be unique to the particular device instance, i.e. no two units must
    supply the same Device ID. The Device ID must not change between sessions
    or power cycles. Good examples is the device's MAC address or unique serial
    number.
    """

    dont_save_metadata_for_playlists = False
    """
    Don't save metadata for local copies of playlists Reduces disk space usage
    at the expense of needing to request metadata from Spotify backend when
    loading list.
    """

    initially_unload_playlists = False
    """
    Avoid loading playlists into RAM on startup. See :attr:`Playlist.in_ram`
    for more details.
    """

    proxy = None
    """
    Url to the proxy server that should be used. The format is
    ``protocol://<host>:port`` (where protocol is http/https/socks4/socks5).
    """

    proxy_password = None
    """
    Password to authenticate with the proxy server.
    """

    proxy_username = None
    """
    Username to authenticate with proxy server.
    """

    settings_location = 'tmp'
    """
    The location where Spotify will write setting files and per-user cache
    items. This includes playlists, track metadata, etc. 'settings_location'
    may be the same path as 'cache_location'. 'settings_location' folder will
    not be created (unlike 'cache_location'), if you don't want to create the
    folder yourself, you can set 'settings_location' to 'cache_location'. 
    """

    tracefile = None
    """
    Path to API trace file.
    """

    user_agent = 'pyspotify-example'
    """
    "User-Agent" for your application - max 255 characters long. The User-Agent
    should be a relevant, customer facing identification of your application.
    """

    userdata = None
    """
    User supplied data for your application.
    """
