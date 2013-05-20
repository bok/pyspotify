# -*- coding: utf-8 -*-

from spotify import capi
from spotify.settings import Settings
from spotify.manager.session import BaseSessionManager

from spotify.util import utf8_str

class Session(object):

    _prefix = 'session'

    def __init__(self):
        self._callbacks = None

    @classmethod
    def _from_cdata(cls, pointer):
        """
        Creates a new instance of this class from a CDATA pointer.
        """
        self = cls()
        self._as_parameter_ = pointer
        return self

    @classmethod
    def create(cls, settings, manager):
        """
        Creates a new Spotify session with the given configuration
        """

        c_config = capi.sp_session_config(
            api_version          = capi.SPOTIFY_API_VERSION,
            cache_location       = utf8_str(settings.cache_location),
            settings_location    = utf8_str(settings.settings_location),
            application_key      = settings.application_key,
            application_key_size = len(settings.application_key),
            user_agent           = utf8_str(settings.user_agent),
            userdata             = settings.userdata,
            compress_playlists   = settings.compress_playlists,
            dont_save_metadata_for_playlists = \
                                   settings.compress_playlists,
            initially_unload_playlists = \
                                   settings.initially_unload_playlists,
            device_id            = utf8_str(settings.device_id),
            proxy                = utf8_str(settings.proxy),
            proxy_username       = utf8_str(settings.proxy_username),
            proxy_password       = utf8_str(settings.proxy_password),
            ca_certs_filename    = utf8_str(settings.ca_certs_filename),
            tracefile            = utf8_str(settings.tracefile),
        )
        callbacks = Session._session_callbacks_from_manager(manager)
        c_callbacks = capi.sp_session_callbacks(**callbacks)

        session = cls._from_cdata(capi.sp_session_create(c_config,
                                                         c_callbacks))
        # Keep a reference to the callbacks to prevent their garbage collection
        session._callbacks = callbacks

        return session

    @staticmethod
    def _session_callbacks_from_manager(manager):
        """
        Returns dictionnary suitable for the creation of a
        capi.sp_session_callbacks object.

        The C callbacks of the structure are created from the corresponding
        methods of the *manager* object.

        .. warning::
            The reference to the returned value must be kept. If the callbacks
            are garbage-collected, their invocation from libspotify will lead
            to a segmentation fault.

        .. note::
            If the *manager* has a method called ``_manager_callback_name``,
            it will be used in place of the method ``callback_name`` for the
            corresponding callback.
        """
        callbacks = {}
        for (func_name, func_type) in capi.sp_session_callbacks._fields_:
            try:
                callbacks[func_name] = \
                        func_type(getattr(manager, '_manager_' + func_name))
            except AttributeError:
                try:
                    callbacks[func_name] = \
                            func_type(getattr(manager, func_name))
                except AttributeError:
                    pass
        return callbacks

    def release(self):
        """
        Release the session. This will clean up all data and connections
        associated with the session.
        """
        return capi.sp_session_release(self)

    def login(self, username, password=None, remember_me=False, blob=None):
        """
        Logs in the specified user to the Spotify service.

        The application must not store any user password in plain text. If
        password storage is needed, the application must store the encrypted
        binary blob corresponding to the user and obtained via the
        :meth:`manager.SpotifySessionManager.credentials_blob_updated` session
        callback. One of ``password`` or ``blob`` must be specified.

        :param username:    the user's login to Spotify Premium
        :type username:     string
        :param password:    the user's password to Spotify Premium
        :type password:     string
        :param remember_me: set this flag if you want libspotify to remember
                            this user
        :type remember_me:  ``bool``
        :param blob:        binary login blob
        :type blob:         ``str``
        """
        return capi.sp_session_login(self, username, password, remember_me,
                                     blob)

    def relogin(self):
        """
        Use this method if you want to re-login the last user who set the
        ``remember_me`` flag in :meth:`Session.login`.
        """
        return capi.sp_session_relogin(self)

    @property
    def remembered_user(self):
        """
        Get username of the user that will be logged in via
        :meth:`Session.relogin`.
        """
        return capi.sp_session_remembered_user(self)

    @property
    def user_name(self):
        """
        Fetches the currently logged in user.
        """
        return capi.sp_session_user_name(self)

    def forget_me(self):
        """
        Remove stored credentials in libspotify. If no credentials are
        currently stored, nothing will happen.
        """
        return capi.sp_session_forget_me(self)

    def logout(self):
        """
        Logs out of the session.
        """
        return capi.sp_session_logout(self)

    def process_events(self):
        """
        Process any pending events.

        .. note::
            Call this fonction from the main thread after getting notified with
            the :meth:`BaseSessionManager.notify_main_thread` callback, or
            after the time indicated by the last call has elapsed.

        :returns: the time (in milliseconds) until you should call this
        function again
        """
        return capi.sp_session_process_events(self)
