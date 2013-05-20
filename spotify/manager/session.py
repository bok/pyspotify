import logging
import ctypes as _ctypes
try:
    import queue
except ImportError:
    import Queue as queue

import spotify
from spotify.settings import Settings

logger = logging.getLogger('pyspotify.manager.session')

class BaseSessionManager(object):
    """
    Class that implements all the session callbacks.

    This class also implements two types of callbacks:

      - wrappers (begining with ``_manager_``) that take care of translating
      CDATA objects (as received from libspotify through ctypes) to pyspotify
      high level structures (such as :class:`Session`)

      - pythonic callbacks, which should be implemented as needed by the
        application in a subclass.
    """

    def _manager_logged_in(self, session, error):
        """
        Wrapper for :meth:`logged_in`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.logged_in(py_session, error)

    def logged_in(self, session, error):
        """
        Callback.

        Called when the login completes. You almost
        certainly want to do something with
        :meth:`session.playlist_container() <spotify.Session.playlist_container>`
        if the login succeded.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param error: an error message, :class:`None` if all went well.
        :type error: string or :class:`None`
        """
        pass

    def _manager_logged_out(self, session):
        """
        Wrapper for :meth:`logged_out`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.logged_out(py_session)

    def logged_out(self, session):
        """
        Callback.

        The user has or has been logged out from Spotify.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_metadata_updated(self, session):
        """
        Wrapper for :meth:`metadata_updated`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.metadata_updated(py_session)

    def metadata_updated(self, session):
        """
        Callback.

        The current user's metadata has been updated.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_connection_error(self, session, error):
        """
        Wrapper for :meth:`connection_error`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.connection_error(py_session, error)

    def connection_error(self, session, error):
        """
        Callback.

        A connection error occured in ``libspotify``.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param error: an error message. If :class:`None`, the connection is
          back.
        :type error: string or :class:`None`
        """
        pass

    def _manager_message_to_user(self, session, message):
        """
        Wrapper for :meth:`message_to_user`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        py_message = message.decode('utf-8')
        return self.message_to_user(py_session, py_message)

    def message_to_user(self, session, message):
        """
        Callback.

        An informative message from ``libspotify``, destinated to the user.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param message: a message.
        :type message: string
        """
        pass

    def _manager_notify_main_thread(self, session):
        """
        Wrapper for :meth:`notify_main_thread`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.notify_main_thread(py_session)

    def notify_main_thread(self, session):
        """
        Callback.

        When this method is called by ``libspotify``, one should call
        :meth:`session.process_events() <spotify.Session.process_events>`.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_music_delivery(self, session, format, frames, num_frames):
        """
        Wrapper for :meth:`music_delivery`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        frame_size = 16 # the only sample type for now is INT16_NATIVE_ENDIAN
        py_frames = (_ctypes.c_int16 * num_frames).from_buffer(frames).value
        sample_type = format.sample_types
        sample_rate = format.sample_rate
        channels = format.channels

        return self.music_delivery(py_session, py_frames, frame_size,
                num_frames, sample_type, sample_rate, channels)

    def music_delivery(self, session, frames, frame_size, num_frames,
            sample_type, sample_rate, channels):
        """
        Callback.

        Called whenever new music data arrives from Spotify.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        .. warning::
            This method must never block.

        :param session: the current session
        :type session: :class:`spotify.Session`
        :param frames: the audio data
        :type frames: :class:`buffer`
        :param frame_size: bytes per frame
        :type frame_size: :class:`int`
        :param num_frames: number of frames in this delivery
        :type num_frames: :class:`int`
        :param sample_type: currently this is always 0 which means 16-bit
            signed native endian integer samples
        :type sample_type: :class:`int`
        :param sample_rate: audio sample rate, in samples per second
        :type sample_rate: :class:`int`
        :param channels: number of audio channels. Currently 1 or 2
        :type channels: :class:`int`
        :return: number of frames consumed
        :rtype: :class:`int`
        """
        pass

    def _manager_play_token_lost(self, session):
        """
        Wrapper for :meth:`play_token_lost`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.play_token_lost(py_session)

    def play_token_lost(self, session):
        """
        Callback.

        The playback stopped because a track was played from another
        application, with the same account.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_log_message(self, session, message):
        """
        Wrapper for :meth:`log_message`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        py_message = message.decode('utf-8')
        return self.log_message(py_session, py_message)

    def log_message(self, session, message):
        """
        Callback.

        A log message from ``libspotify``.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param message: the message.
        :type message: string
        """
        pass

    def _manager_end_of_track(self, session):
        """
        Wrapper for :meth:`end_of_track`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.end_of_track(py_session)

    def end_of_track(self, session):
        """
        Callback.

        Playback has reached the end of the current track.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_streaming_error(self, session, error):
        """
        Wrapper for :meth:`streaming_error`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.streaming_error(py_session, error)

    def streaming_error(self, session, error):
        """
        Callback.

        Streaming error. Called when streaming cannot start or continue.

        .. note::
            This function is invoked from the main thread

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param error: the error code
        :type session: :class:`int`
        """
        pass

    def _manager_userinfo_updated(self, session):
        """
        Wrapper for :meth:`userinfo_updated`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.userinfo_updated(py_session)

    def userinfo_updated(self, session):
        """
        Callback.

        Called after user info (anything related to :class:`User` objects)
        have been updated.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_start_playback(self, session):
        """
        Wrapper for :meth:`start_playback`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.start_playback(py_session)

    def start_playback(self, session):
        """
        Callback.

        Called when audio playback should start.

        ..note::
            For this to work correctly the application must also implement
            :meth:`get_audio_buffer_stats`.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        .. warning::
            This method must never block.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_stop_playback(self, session):
        """
        Wrapper for :meth:`stop_playback`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.stop_playback(py_session)

    def stop_playback(self, session):
        """
        Callback.

        Called when audio playback should stop.

        ..note::
            For this to work correctly the application must also implement
            :meth:`get_audio_buffer_stats`.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        .. warning::
            This method must never block.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_get_audio_buffer_stats(self, session, stats):
        """
        Wrapper for :meth:`get_audio_buffer_stats`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        dic_stats = { 'samples': 0, 'stutter': 0 }
        self.get_audio_buffer_stats(py_session, dic_stats)
        stats.samples = dic_stats['samples']
        stats.stutter = dic_stats['stutter']

    def get_audio_buffer_stats(self, session, stats):
        """
        Callback.

        Called to query application about its audio buffer.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        .. warning::
            This method must never block.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param stats: buffer information to be filled by the application
        :type session: :class:`dic`
        """
        pass

    def _manager_offline_status_updated(self, session):
        """
        Wrapper for :meth:`offline_status_updated`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.offline_status_updated(py_session)

    def offline_status_updated(self, session):
        """
        Callback.

        Called when offline synchronization status is updated.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_offline_error(self, session, error):
        """
        Wrapper for :meth:`offline_error`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.offline_error(py_session, error)

    def offline_error(self, session, error):
        """
        Callback.

        Called when offline synchronization cannot start or continue.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param error: the error code
        :type session: :class:`int`
        """
        pass

    def _manager_credentials_blob_updated(self, session, blob):
        """
        Wrapper for :meth:`credentials_blob_updated`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.credentials_blob_updated(py_session, blob)

    def credentials_blob_updated(self, session, blob):
        """
        Callback.

        Called when storable credentials have been updated, usually called when
        we have connected to the AP.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param blob: a string which contains an encrypted token that can be
            stored safely on disk instead of storing plaintext passwords.
        """
        pass

    def _manager_connectionstate_updated(self, session):
        """
        Wrapper for :meth:`connectionstate_updated`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.connectionstate_updated(py_session)

    def connectionstate_updated(self, session):
        """
        Callback.

        Called when the connection state has updated - such as when logging in,
        going offline, etc.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        pass

    def _manager_scrobble_error(self, session, error):
        """
        Wrapper for :meth:`scrobble_error`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.scrobble_error(py_session, error)

    def scrobble_error(self, session, error):
        """
        Callback.

        Called when there is a scrobble error event.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param error: the error code
        :type session: :class:`int`, currently
                       ``capi.SP_ERROR_LASTFM_AUTH_ERROR``
        """
        pass

    def _manager_private_session_mode_changed(self, session, is_private):
        """
        Wrapper for :meth:`private_session_mode_changed`.
        """
        py_session = spotify.session.Session._from_cdata(session)
        return self.private_session_mode_changed(py_session, (is_private != 0))

    def private_session_mode_changed(self, session, is_private):
        """
        Callback.

        Called when there is a change in the private session mode.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        :param is_private: True if in private session, False otherwhise
        :type is_private: ``bool``
        """
        pass

class SpotifySessionManager(BaseSessionManager):
    """
    Client for Spotify. Inherit from this class to have your callbacks
    called on the appropriate events.

    Exceptions raised in your callback handlers will be displayed on the
    standard error output (stderr).

    When logging in a user, the application can pass one of:
        - `username` + `password`: standard login using a plaintext password
        - nothing: logs in the last user which credentials have been stored
          using `remember_me`.
        - `username` + `login_blob`: the blob is encrypted data from
          *libspotify*, for when a multi-user application wants to use
          the re-login feature. The blob is obtained from the
          :meth:`credentials_blob_updated` callback after a successful
          login to the Spotify AP.

    When behind a proxy, the application can specify:
        - `proxy`: url to the proxy server that should be used. The format
            is ``protocol://<host>:port`` (where protocol is
            ``http/https/socks4/socks5``)
        - `proxy_username`: username to authenticate with the proxy server.
        - `proxy_password`: password to authenticate with the proxy server.
    """

    cache_location = 'tmp'
    settings_location = 'tmp'
    application_key = None
    appkey_file = 'spotify_appkey.key'
    user_agent = 'pyspotify-example'

    def __init__(self, username=None, password=None, remember_me=False,
                 login_blob='', proxy=None, proxy_username=None,
                 proxy_password=None):
        self._cmdqueue = queue.Queue()

        # Session settings
        self.settings = Settings()
        if self.application_key is None:
            self.application_key = open(self.appkey_file, 'rb').read()
        self.settings.application_key   = self.application_key
        self.settings.cache_location    = self.cache_location
        self.settings.settings_location = self.settings_location
        self.settings.user_agent        = self.user_agent
        self.settings.proxy             = proxy
        self.settings.proxy_username    = proxy_username
        self.settings.proxy_password    = proxy_password

        # Connection settings
        self.username = username
        self.password = password
        self.remember_me = remember_me
        self.login_blob = login_blob

        # Create session
        self.session = spotify.Session.create(self.settings, self)

    def connect(self):
        """
        Connect to the Spotify API using the given username and password.
        If ``username`` is ``None``, reconnection of the last user will
        be attempted.

        This method does not return before we disconnect from the Spotify
        service.
        """
        if self.username is None:
            self.session.relogin()
        else:
            self.session.login(self.username, self.password,
                               self.remember_me)
        self.loop(self.session) # returns on logged out

    def loop(self, session):
        """
        The main loop.

        Processes events from ``libspotify`` and turns some of them into
        callback calls.
        """
        running = True
        timeout = 0
        while running:
            try:
                message = self._cmdqueue.get(timeout=timeout)
                if message.get('command') == 'music_delivery':
                    num_frames = self.music_delivery_safe(
                        session, *message['args'])
                    message['reply_to'].put(num_frames)
                elif message.get('command') == 'process_events':
                    logger.debug('Got message; processing events')
                    timeout = session.process_events() / 1000.0
                    logger.debug('Will wait %.3fs for next message', timeout)
                elif message.get('command') == 'disconnect':
                    logger.debug('Got message; disconnecting')
                    session.logout()
                elif message.get('command') == 'stop':
                    logger.debug('Got message; stopping main loop')
                    running = False
                else:
                    raise ValueError('Unknown message type')
            except queue.Empty:
                logger.debug(
                    'No message received before timeout. Processing events')
                timeout = session.process_events() / 1000.0
                logger.debug('Will wait %.3fs for next message', timeout)

    def disconnect(self):
        """
        Terminate the current Spotify session.
        """
        self._cmdqueue.put({'command': 'disconnect'})

    def _manager_logged_out(self, session):
        """
        Callback.

        This is a wrapper method around `logged_out` that
        also stops the manager's main loop. Don't override
        this method.

        See :meth:`BaseSessionManager.logged_out` for additional
        documentation.

        :param session: the current session.
        :type session: :class:`spotify.Session`
        """
        self._cmdqueue.put({'command': 'stop'})
        # Call the parent method to benefit from the translation of parameters
        # before calling self.logged_out()
        BaseSessionManager._manager_logged_out(self, session)

    def notify_main_thread(self, session=None):
        """
        Callback.

        If you use the :class:`SessionManager`'s default loop, the default
        implementation of this method does the job. Though, if you implement
        your own loop for handling Spotify events, you'll need to override this
        method.

        See :meth:`BaseSessionManager.notify_main_thread` for additional
        documentation.
        """
        self._cmdqueue.put({'command': 'process_events'})

    def music_delivery(self, session, frames, frame_size, num_frames,
            sample_type, sample_rate, channels):
        """
        Callback.

        Called whenever new music data arrives from Spotify.

        You should override this method *or* :meth:`music_delivery_safe`, not both.

        .. warning::
            This method is called from an internal thread in libspotify. You
            should make sure *not* to use the Spotify API from within it, as
            libspotify isn't thread safe.

        See :meth:`BaseSessionManager.music_delivery` for additional
        documentation.

        """
        try:
            future = queue.Queue()
            self._cmdqueue.put({
                'command': 'music_delivery',
                'args': (frames, frame_size, num_frames, sample_type, sample_rate,
                    channels),
                'reply_to': future,
            }, block=False)
            return future.get()
        except queue.Full:
            return 0

    def music_delivery_safe(self, session, frames, frame_size, num_frames,
            sample_type, sample_rate, channels):
        """
        This method does the same as :meth:`music_delivery`, except that it's
        called from the :class:`SpotifySessionManager` loop. You can safely use
        Spotify APIs from within this method.

        You should override this method *or* :meth:`music_delivery`, not both.
        """
        return 0
