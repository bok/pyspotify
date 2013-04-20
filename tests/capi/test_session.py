import ctypes
import threading
import unittest

from spotify import capi, mock
from spotify.mock import capi as mockapi

class CAPISessionEnumAndStructTest(unittest.TestCase):
    def test_sp_connectionstate_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_CONNECTION_STATE_LOGGED_OUT, 0)
        self.assertEqual(capi.SP_CONNECTION_STATE_LOGGED_IN, 1)
        self.assertEqual(capi.SP_CONNECTION_STATE_DISCONNECTED, 2)
        self.assertEqual(capi.SP_CONNECTION_STATE_UNDEFINED, 3)
        self.assertEqual(capi.SP_CONNECTION_STATE_OFFLINE, 4)

    def test_sp_sampletype_is_ctypes_c_uint(self):
        self.assertEqual(capi.sp_sampletype, ctypes.c_int)

    def test_sp_sampletype_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_SAMPLETYPE_INT16_NATIVE_ENDIAN, 0)

    def test_sp_audioformat_struct_can_be_created_and_read_from(self):
        audioformat = capi.sp_audioformat(
            sample_type=capi.SP_SAMPLETYPE_INT16_NATIVE_ENDIAN,
            sample_rate=44100,
            channels=2)
        self.assertEqual(audioformat.sample_type,
            capi.SP_SAMPLETYPE_INT16_NATIVE_ENDIAN)
        self.assertEqual(audioformat.sample_rate, 44100)
        self.assertEqual(audioformat.channels, 2)

    def test_sp_bitrate_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_BITRATE_160k, 0)
        self.assertEqual(capi.SP_BITRATE_320k, 1)
        self.assertEqual(capi.SP_BITRATE_96k, 2)

    def test_sp_playlist_type_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_PLAYLIST_TYPE_PLAYLIST, 0)
        self.assertEqual(capi.SP_PLAYLIST_TYPE_START_FOLDER, 1)
        self.assertEqual(capi.SP_PLAYLIST_TYPE_END_FOLDER, 2)
        self.assertEqual(capi.SP_PLAYLIST_TYPE_PLACEHOLDER, 3)

    def test_sp_playlist_offline_status_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_PLAYLIST_OFFLINE_STATUS_NO, 0)
        self.assertEqual(capi.SP_PLAYLIST_OFFLINE_STATUS_YES, 1)
        self.assertEqual(capi.SP_PLAYLIST_OFFLINE_STATUS_DOWNLOADING, 2)
        self.assertEqual(capi.SP_PLAYLIST_OFFLINE_STATUS_WAITING, 3)

    def test_sp_availability_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_TRACK_AVAILABILITY_UNAVAILABLE, 0)
        self.assertEqual(capi.SP_TRACK_AVAILABILITY_AVAILABLE, 1)
        self.assertEqual(capi.SP_TRACK_AVAILABILITY_NOT_STREAMABLE, 2)
        self.assertEqual(capi.SP_TRACK_AVAILABILITY_BANNED_BY_ARTIST, 3)

    def test_sp_track_offline_status_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_TRACK_OFFLINE_NO, 0)
        self.assertEqual(capi.SP_TRACK_OFFLINE_WAITING, 1)
        self.assertEqual(capi.SP_TRACK_OFFLINE_DOWNLOADING, 2)
        self.assertEqual(capi.SP_TRACK_OFFLINE_DONE, 3)
        self.assertEqual(capi.SP_TRACK_OFFLINE_ERROR, 4)
        self.assertEqual(capi.SP_TRACK_OFFLINE_DONE_EXPIRED, 5)
        self.assertEqual(capi.SP_TRACK_OFFLINE_LIMIT_EXCEEDED, 6)
        self.assertEqual(capi.SP_TRACK_OFFLINE_DONE_RESYNC, 7)

    def test_sp_audio_buffer_stats_struct_can_be_created_and_read_from(self):
        stats = capi.sp_audio_buffer_stats(samples=100, stutter=0)
        self.assertEqual(stats.samples, 100)
        self.assertEqual(stats.stutter, 0)

    def test_sp_subscribers_struct_can_be_created_and_read_from(self):
        users = [s.encode('utf-8') for s in ['foo', 'bar', 'baz']]
        subscribers = capi.sp_subscribers(count=len(users),
            subscribers=(ctypes.c_char_p * len(users))(*users))
        self.assertEqual(subscribers.count, 3)
        self.assertSequenceEqual(subscribers.subscribers[0:3], users)

    def test_sp_connection_type_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_CONNECTION_TYPE_UNKNOWN, 0)
        self.assertEqual(capi.SP_CONNECTION_TYPE_NONE, 1)
        self.assertEqual(capi.SP_CONNECTION_TYPE_MOBILE, 2)
        self.assertEqual(capi.SP_CONNECTION_TYPE_MOBILE_ROAMING, 3)
        self.assertEqual(capi.SP_CONNECTION_TYPE_WIFI, 4)
        self.assertEqual(capi.SP_CONNECTION_TYPE_WIRED, 5)

    def test_sp_connection_rules_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_CONNECTION_RULE_NETWORK, 0x1)
        self.assertEqual(capi.SP_CONNECTION_RULE_NETWORK_IF_ROAMING, 0x2)
        self.assertEqual(capi.SP_CONNECTION_RULE_ALLOW_SYNC_OVER_MOBILE, 0x4)
        self.assertEqual(capi.SP_CONNECTION_RULE_ALLOW_SYNC_OVER_WIFI, 0x8)

    def test_sp_artistbrowse_type_enum_has_correct_enumeration(self):
        self.assertEqual(capi.SP_ARTISTBROWSE_FULL, 0)
        self.assertEqual(capi.SP_ARTISTBROWSE_NO_TRACKS, 1)
        self.assertEqual(capi.SP_ARTISTBROWSE_NO_ALBUMS, 2)

    def test_sp_offline_sync_status_can_be_created_and_read_from(self):
        status = capi.sp_offline_sync_status(
            queued_tracks=7,
            queued_bytes=64000,
            done_tracks=101,
            done_bytes=564000,
            copied_tracks=13,
            copied_bytes=143000,
            willnotcopy_tracks=1,
            error_tracks=2,
            syncing=True,
        )
        self.assertEqual(status.queued_tracks, 7)
        self.assertEqual(status.queued_bytes, 64000)
        self.assertEqual(status.done_tracks, 101)
        self.assertEqual(status.done_bytes, 564000)
        self.assertEqual(status.copied_tracks, 13)
        self.assertEqual(status.copied_bytes, 143000)
        self.assertEqual(status.willnotcopy_tracks, 1)
        self.assertEqual(status.error_tracks, 2)
        self.assertEqual(status.syncing, True)

    def test_sp_offline_sync_status_raises_exc_on_wrong_arg_types(self):
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            queued_tracks='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            queued_bytes='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            done_tracks='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            done_bytes='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            copied_tracks='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            willnotcopy_tracks='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            error_tracks='not an integer')
        self.assertRaises(TypeError, capi.sp_offline_sync_status,
            syncing='not an integer')


class CAPISessionCallbackTest(unittest.TestCase):
    def test_SP_SESSION_LOGGED_IN_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_LOGGED_IN_FUNC(lambda session, error: None)
        self.assertEqual(callback(None, 0), None)

    def test_SP_SESSION_LOGGED_OUT_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_LOGGED_OUT_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_METADATA_UPDATED_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_METADATA_UPDATED_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_CONNECTION_ERROR_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_CONNECTION_ERROR_FUNC(
            lambda session, error: None)
        self.assertEqual(callback(None, 0), None)

    def test_SP_SESSION_MESSAGE_TO_USER_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_MESSAGE_TO_USER_FUNC(
            lambda session, message: None)
        self.assertEqual(callback(None, 'msg'.encode('utf-8')), None)

    def test_SP_SESSION_NOTIFY_MAIN_THREAD_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_NOTIFY_MAIN_THREAD_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_MUSIC_DELIVERY_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_MUSIC_DELIVERY_FUNC(lambda session,
            audioformat, frames, num_frames: 7)
        self.assertEqual(callback(None, None, None, 10), 7)

    def test_SP_SESSION_PLAY_TOKEN_LOST_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_PLAY_TOKEN_LOST_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_LOG_MESSAGE_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_LOG_MESSAGE_FUNC(lambda session, data: None)
        self.assertEqual(callback(None, 'msg'.encode('utf-8')), None)

    def test_SP_SESSION_END_OF_TRACK_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_END_OF_TRACK_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_STREAMING_ERROR_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_STREAMING_ERROR_FUNC(
            lambda session, error: None)
        self.assertEqual(callback(None, 0), None)

    def test_SP_SESSION_USERINFO_UPDATED_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_USERINFO_UPDATED_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_START_PLAYBACK_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_START_PLAYBACK_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_STOP_PLAYBACK_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_STOP_PLAYBACK_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_GET_AUDIO_BUFFER_STATS_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_GET_AUDIO_BUFFER_STATS_FUNC(
            lambda session, stats: None)
        self.assertEqual(callback(None, None), None)

    def test_SP_SESSION_OFFLINE_STATUS_UPDATED_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_OFFLINE_STATUS_UPDATED_FUNC(lambda session: None)
        self.assertEqual(callback(None), None)

    def test_SP_SESSION_OFFLINE_ERROR_FUNC_can_wrap_callback(self):
        callback = capi.SP_SESSION_OFFLINE_ERROR_FUNC(lambda session, error: None)
        self.assertEqual(callback(None, 0), None)

    def test_sp_session_callbacks_can_be_created_and_read_from(self):
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(lambda *args: None),
            logged_out=capi.SP_SESSION_LOGGED_OUT_FUNC(lambda *args: None),
            metadata_updated=capi.SP_SESSION_METADATA_UPDATED_FUNC(
                lambda *args: None),
            connection_error=capi.SP_SESSION_CONNECTION_ERROR_FUNC(
                lambda *args: None),
            message_to_user=capi.SP_SESSION_MESSAGE_TO_USER_FUNC(
                lambda *args: None),
            notify_main_thread=capi.SP_SESSION_NOTIFY_MAIN_THREAD_FUNC(
                lambda *args: None),
            music_delivery=capi.SP_SESSION_MUSIC_DELIVERY_FUNC(
                lambda *args: 7),
            play_token_lost=capi.SP_SESSION_PLAY_TOKEN_LOST_FUNC(
                lambda *args: None),
            log_message=capi.SP_SESSION_LOG_MESSAGE_FUNC(
                lambda *args: None),
            end_of_track=capi.SP_SESSION_END_OF_TRACK_FUNC(
                lambda *args: None),
            streaming_error=capi.SP_SESSION_STREAMING_ERROR_FUNC(
                lambda *args: None),
            userinfo_updated=capi.SP_SESSION_USERINFO_UPDATED_FUNC(
                lambda *args: None),
            start_playback=capi.SP_SESSION_START_PLAYBACK_FUNC(
                lambda *args: None),
            stop_playback=capi.SP_SESSION_STOP_PLAYBACK_FUNC(
                lambda *args: None),
            get_audio_buffer_stats=capi.SP_SESSION_GET_AUDIO_BUFFER_STATS_FUNC(
                lambda *args: None),
            offline_status_updated=capi.SP_SESSION_OFFLINE_STATUS_UPDATED_FUNC(
                lambda *args: None),
            offline_error=capi.SP_SESSION_OFFLINE_ERROR_FUNC(
                lambda *args: None),
        )
        self.assertEqual(callbacks.logged_in(None, 0), None)
        self.assertEqual(callbacks.logged_out(None), None)
        self.assertEqual(callbacks.metadata_updated(None), None)
        self.assertEqual(callbacks.connection_error(None, 0), None)
        self.assertEqual(callbacks.message_to_user(None, 'msg'.encode('utf-8')), None)
        self.assertEqual(callbacks.notify_main_thread(None), None)
        self.assertEqual(callbacks.music_delivery(None, None, None, 0), 7)
        self.assertEqual(callbacks.play_token_lost(None), None)
        self.assertEqual(callbacks.log_message(None, 'msg'.encode('utf-8')), None)
        self.assertEqual(callbacks.end_of_track(None), None)
        self.assertEqual(callbacks.streaming_error(None, 0), None)
        self.assertEqual(callbacks.userinfo_updated(None), None)
        self.assertEqual(callbacks.start_playback(None), None)
        self.assertEqual(callbacks.stop_playback(None), None)
        self.assertEqual(callbacks.get_audio_buffer_stats(None, None), None)
        self.assertEqual(callbacks.offline_status_updated(None), None)
        self.assertEqual(callbacks.offline_error(None, 0), None)

    def test_sp_session_callbacks_raises_exc_on_wrong_arg_types(self):
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            logged_in='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            logged_out='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            metadata_updated='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            connection_error='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            message_to_user='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            notify_main_thread='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            music_delivery='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            play_token_lost='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            log_message='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            end_of_track='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            streaming_error='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            userinfo_updated='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            start_playback='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            stop_playback='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            get_audio_buffer_stats='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            offline_status_updated='not a function')
        self.assertRaises(TypeError, capi.sp_session_callbacks,
            offline_error='not a function')


class CAPISessionConfigTest(unittest.TestCase):
    def test_sp_session_config_can_be_created_and_read_from(self):
        callbacks = capi.sp_session_callbacks()
        config = capi.sp_session_config(
            api_version=12,
            cache_location='foo'.encode('utf-8'),
            settings_location='bar'.encode('utf-8'),
            application_key=None,
            application_key_size=0,
            user_agent='baz'.encode('utf-8'),
            callbacks=ctypes.pointer(callbacks),
            compress_playlists=True,
            dont_save_metadata_for_playlists=True,
            initially_unload_playlists=True,
            device_id='qux'.encode('utf-8'),
            tracefile='quux'.encode('utf-8'),
        )
        self.assertEqual(config.api_version, 12)
        self.assertEqual(config.cache_location, 'foo'.encode('utf-8'))
        self.assertEqual(config.settings_location, 'bar'.encode('utf-8'))
        self.assertEqual(config.application_key, None)
        self.assertEqual(config.application_key_size, 0)
        self.assertEqual(config.user_agent, 'baz'.encode('utf-8'))
        self.assertEqual(type(config.callbacks[0]), type(callbacks))
        self.assertEqual(config.compress_playlists, True)
        self.assertEqual(config.dont_save_metadata_for_playlists, True)
        self.assertEqual(config.initially_unload_playlists, True)
        self.assertEqual(config.device_id, 'qux'.encode('utf-8'))
        self.assertEqual(config.tracefile, 'quux'.encode('utf-8'))

    def test_sp_session_config_raises_exc_on_wrong_arg_types(self):
        self.assertRaises(TypeError, capi.sp_session_config,
            api_version='not an integer')
        self.assertRaises(TypeError, capi.sp_session_config,
            cache_location=1.0)
        self.assertRaises(TypeError, capi.sp_session_config,
            settings_location=1.0)
        self.assertRaises(TypeError, capi.sp_session_config,
            application_key=1.0)
        self.assertRaises(TypeError, capi.sp_session_config,
            application_key_size='not an integer')
        self.assertRaises(TypeError, capi.sp_session_config,
            user_agent=1.0)
        self.assertRaises(TypeError, capi.sp_session_config,
            callbacks='not a sp_session_callbacks pointer')
        self.assertRaises(TypeError, capi.sp_session_config,
            compress_playlists='not a bool')
        self.assertRaises(TypeError, capi.sp_session_config,
            dont_save_metadata_for_playlists='not a bool')
        self.assertRaises(TypeError, capi.sp_session_config,
            initially_unload_playlists='not a bool')
        self.assertRaises(TypeError, capi.sp_session_config,
            device_id=1.0)
        self.assertRaises(TypeError, capi.sp_session_config,
            tracefile=1.0)


class CAPISessionCreationTest(unittest.TestCase):
    def test_sp_session_create(self):
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks()
        session = capi.sp_session_create(config, callbacks)
        self.assertEqual(type(session), ctypes.POINTER(capi.sp_session))

    def test_sp_session_create_fails_with_invalid_app_key(self):
        application_key = b'appkey_bad'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks()
        self.assertRaises(capi.SpError,
            capi.sp_session_create, config, callbacks)

    def test_sp_session_create_fails_with_invalid_arg_count(self):
        self.assertRaises(TypeError, capi.sp_session_create)

    def test_sp_session_create_fails_with_invalid_arg_type(self):
        self.assertRaises(TypeError, capi.sp_session_create, 1.0, None)


class CAPISessionLoginTest(unittest.TestCase):
    def test_sp_session_login(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assert_(self.logged_in_called.is_set())

class CAPISessionReleaseTest(unittest.TestCase):
    def test_sp_session_release(self):
        session = mock.Session()

        capi.sp_session_release(session)

class CAPISessionReloginTest(unittest.TestCase):
    def test_sp_session_relogin(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=True, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        self.logged_in_called.clear()
        capi.sp_session_relogin(session)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())

    def test_sp_session_relogin_no_credentials(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        self.logged_in_called.clear()
        with self.assertRaises(capi.SpError) as err:
            capi.sp_session_relogin(session)
            self.assertEquals(err.arg, (capi.SP_ERROR_NO_CREDENTIALS,))

class CAPISessionRememberedUserTest(unittest.TestCase):
    def test_sp_session_remembered_user(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=True, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        user = capi.sp_session_remembered_user(session)
        self.assertEquals(user, 'alice')

    def test_sp_session_remembered_user_no_credentials(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        user = capi.sp_session_remembered_user(session)
        self.assertIsNone(user)

class CAPISessionUserNameTest(unittest.TestCase):
    def test_sp_session_user_name(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        user_name = capi.sp_session_user_name(session)
        self.assertEquals(user_name, 'alice')

class CAPISessionForgetMeTest(unittest.TestCase):
    def test_sp_session_forget_me(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=True, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        capi.sp_session_forget_me(session)
        user = capi.sp_session_remembered_user(session)
        self.assertIsNone(user)

class CAPISessionUserTest(unittest.TestCase):
    @unittest.skip('TODO: Implement sp_user_canonical_name in capi')
    def test_sp_session_user(self):
        self.logged_in_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        user = capi.sp_session_user(session)
        self.assertIsInstance(user, ctypes.POINTER(capi.sp_user))
        self.assertEquals(capi.sp_user_canonical_name(user), 'alice')

class CAPISessionLogoutTest(unittest.TestCase):
    def test_sp_session_logout(self):
        self.logged_in_called = threading.Event()
        self.logged_out_called = threading.Event()
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set()),
            logged_out=capi.SP_SESSION_LOGGED_OUT_FUNC(
                lambda *a: self.logged_out_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        capi.sp_session_login(session,
            username='alice', password='secret', remember_me=False, blob=None)

        self.logged_in_called.wait(1)
        self.assertTrue(self.logged_in_called.is_set())
        capi.sp_session_logout(session)
        self.logged_out_called.wait(1)
        self.assertTrue(self.logged_out_called.is_set())

class CAPISessionFlushCachesTest(unittest.TestCase):
    def test_sp_session_flush_caches(self):
        session = mock.Session()

        capi.sp_session_flush_caches(session)

class CAPISessionConnectionStateTest(unittest.TestCase):
    def test_sp_session_connectionstate(self):
        session = mock.Session(connection_state=
                               capi.SP_CONNECTION_STATE_LOGGED_OUT)

        state = capi.sp_session_connectionstate(session)
        self.assertEquals(state, capi.SP_CONNECTION_STATE_LOGGED_OUT)

        session = mock.Session(connection_state=
                               capi.SP_CONNECTION_STATE_LOGGED_IN)
        state = capi.sp_session_connectionstate(session)
        self.assertEquals(state, capi.SP_CONNECTION_STATE_LOGGED_IN)

class CAPISessionUserdataTest(unittest.TestCase):
    def test_sp_session_userdata(self):
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key),
            userdata='pipo')
        session = mock.Session(config=config)

        userdata = capi.sp_session_userdata(session)
        self.assertIs(userdata, config.userdata)

class CAPISessionSetCacheSizeTest(unittest.TestCase):
    def test_sp_session_set_cache_size(self):
        session = mock.Session()

        capi.sp_session_set_cache_size(session, 10)

class CAPISessionProcessEventsTest(unittest.TestCase):
    def test_sp_session_process_events(self):
        application_key = b'appkey_good'
        config = capi.sp_session_config(
            application_key=application_key,
            application_key_size=len(application_key))
        callbacks = capi.sp_session_callbacks(
            logged_in=capi.SP_SESSION_LOGGED_IN_FUNC(
                lambda *a: self.logged_in_called.set())
        )
        session = capi.sp_session_create(config, callbacks)

        next_timeout = capi.sp_session_process_events(session)

        self.assertEquals(next_timeout, 1)

class CAPISessionPlayerTests(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_track_create')
    def test_sp_session_player_load(self):
        session = mock.Session()
        track = mock.Track()

        capi.sp_session_player_load(session, track)

    def test_sp_session_player_seek(self):
        session = mock.Session()

        capi.sp_session_player_seek(session, 42)

    def test_sp_session_player_play(self):
        session = mock.Session()

        capi.sp_session_player_play(session, True)
        capi.sp_session_player_play(session, False)

    def test_sp_session_player_unload(self):
        session = mock.Session()

        capi.sp_session_player_unload(session)

    @unittest.skip('TODO: implement mocksp_track_create')
    def test_sp_session_player_prefetch(self):
        session = mock.Session()
        track = mock.Track()

        capi.sp_session_player_prefetch(session, track)

class CAPISessionPlaylistcontainerTest(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_registry_add')
    def test_sp_session_playlistcontainer(self):
        session = mock.Session()

        pc = capi.sp_session_playlistcontainer(session)
        self.assertIsInstance(pc, ctypes.POINTER(capi.sp_playlistcontainer))
        self.assertTrue(pc) # TODO implement libmockspotify's registry_add

class CAPISessionInboxCreateTest(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_playlist_*')
    def test_sp_session_inbox_create(self):
        playlist = mock.Playlist()
        session = mock.Session(inbox=playlist)

        inbox = capi.sp_session_inbox_create(session)
        self.assertIsInstance(inbox, ctypes.POINTER(capi.sp_playlist))
        self.assertEquals(inbox, playlist)

class CAPISessionStarredCreateTest(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_registry_add')
    def test_sp_session_starred_create_logged_in(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_IN)

        starred = capi.sp_session_starred_create(session)
        self.assertIsInstance(starred, ctypes.POINTER(capi.sp_playlist))
        self.assertTrue(starred)

    def test_sp_session_starred_create_logged_out(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_OUT)

        starred = capi.sp_session_starred_create(session)
        self.assertFalse(starred)

class CAPISessionStarredForUserCreateTest(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_registry_add')
    def test_sp_session_starred_for_user_create_logged_in(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_IN)

        starred = capi.sp_session_starred_for_user_create(session,
                                                        'foo'.encode('utf-8'))
        self.assertIsInstance(starred, ctypes.POINTER(capi.sp_playlist))
        self.assertTrue(starred)

    def test_sp_session_starred_for_user_create_logged_out(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_OUT)

        starred = capi.sp_session_starred_for_user_create(session,
                                                        'foo'.encode('utf-8'))
        self.assertIsInstance(starred, ctypes.POINTER(capi.sp_playlist))
        self.assertFalse(starred)

class CAPISessionPublishedcontainerForUserCreateTest(unittest.TestCase):
    @unittest.skip('TODO: implement mocksp_registry_add')
    def test_sp_session_publishedcontainer_for_user_create_logged_in(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_IN)

        publishedcontainer = \
            capi.sp_session_publishedcontainer_for_user_create(session,
                                                        'foo'.encode('utf-8'))
        self.assertIsInstance(publishedcontainer,
                ctypes.POINTER(capi.sp_playlistcontainer))
        self.assertTrue(publishedcontainer)

    def test_sp_session_publishedcontainer_for_user_create_logged_out(self):
        session = \
        mock.Session(connection_state=capi.SP_CONNECTION_STATE_LOGGED_OUT)

        publishedcontainer = \
            capi.sp_session_publishedcontainer_for_user_create(session,
                                                        'foo'.encode('utf-8'))
        self.assertIsInstance(publishedcontainer,
                ctypes.POINTER(capi.sp_playlistcontainer))
        self.assertFalse(publishedcontainer)

class CAPISessionPreferredBitrateTest(unittest.TestCase):
    def test_sp_session_preferred_bitrate(self):
        session = mock.Session()

        capi.sp_session_preferred_bitrate(session, capi.SP_BITRATE_96k)
        capi.sp_session_preferred_bitrate(session, capi.SP_BITRATE_160k)
        capi.sp_session_preferred_bitrate(session, capi.SP_BITRATE_320k)

class CAPISessionPreferredOfflineBitrateTest(unittest.TestCase):
    def test_sp_session_preferred_offline_bitrate(self):
        session = mock.Session()

        capi.sp_session_preferred_offline_bitrate(session,
                                                  capi.SP_BITRATE_96k, 1)
        capi.sp_session_preferred_offline_bitrate(session,
                                                  capi.SP_BITRATE_160k, True)
        capi.sp_session_preferred_offline_bitrate(session,
                                                  capi.SP_BITRATE_160k, False)

class CAPISessionGetSetVolumeNormalizationTest(unittest.TestCase):
    def test_sp_get_set_volume_normalization(self):
        session = mock.Session()

        capi.sp_session_set_volume_normalization(session, True)
        norm = capi.sp_session_get_volume_normalization(session)
        self.assertIsInstance(norm, bool)
        self.assertTrue(norm)

        capi.sp_session_set_volume_normalization(session, False)
        norm = capi.sp_session_get_volume_normalization(session)
        self.assertIsInstance(norm, bool)
        self.assertFalse(norm)

class CAPISessionIsSetPrivateSessionTest(unittest.TestCase):
    def test_sp_is_set_private_session(self):
        session = mock.Session()

        capi.sp_session_set_private_session(session, True)
        priv = capi.sp_session_is_private_session(session)
        self.assertIsInstance(priv, bool)
        self.assertTrue(priv)

        capi.sp_session_set_private_session(session, False)
        priv = capi.sp_session_is_private_session(session)
        self.assertIsInstance(priv, bool)
        self.assertFalse(priv)

class CAPISessionIsSetScrobblingTest(unittest.TestCase):
    def test_sp_session_is_set_scrobbling(self):
        session = mock.Session()

        capi.sp_session_set_scrobbling(session,
                capi.SP_SOCIAL_PROVIDER_LASTFM,
                capi.SP_SCROBBLING_STATE_GLOBAL_ENABLED)
        priv = capi.sp_session_is_scrobbling(session,
                capi.SP_SOCIAL_PROVIDER_LASTFM)
        self.assertEquals(priv, capi.SP_SCROBBLING_STATE_GLOBAL_ENABLED)

        capi.sp_session_set_scrobbling(session,
                capi.SP_SOCIAL_PROVIDER_FACEBOOK,
                capi.SP_SCROBBLING_STATE_LOCAL_DISABLED)
        priv = capi.sp_session_is_scrobbling(session,
                capi.SP_SOCIAL_PROVIDER_FACEBOOK)
        self.assertEquals(priv, capi.SP_SCROBBLING_STATE_LOCAL_DISABLED)

    def test_sp_session_is_set_scrobbling_invalid(self):
        session = mock.Session()

        with self.assertRaises(capi.SpError) as e:
            res = capi.sp_session_is_scrobbling(session, 42)
        self.assertEquals(e.exception.code, capi.SP_ERROR_INVALID_ARGUMENT)

        with self.assertRaises(capi.SpError) as e:
            res = capi.sp_session_set_scrobbling(session, 42,
                    capi.SP_SCROBBLING_STATE_LOCAL_ENABLED)
        self.assertEquals(e.exception.code, capi.SP_ERROR_INVALID_ARGUMENT)

        with self.assertRaises(capi.SpError) as e:
            res = capi.sp_session_set_scrobbling(session,
                    capi.SP_SOCIAL_PROVIDER_LASTFM, 1337)
        self.assertEquals(e.exception.code, capi.SP_ERROR_INVALID_ARGUMENT)

class CAPISessionIsScrobblingPossibleTest(unittest.TestCase):
    def test_sp_session_is_scrobbling_possible(self):
        session = mock.Session(scrobbling_possible = 0b101)

        res = capi.sp_session_is_scrobbling_possible(session,
                capi.SP_SOCIAL_PROVIDER_SPOTIFY)
        self.assertIsInstance(res, bool)
        self.assertTrue(res);

        res = capi.sp_session_is_scrobbling_possible(session,
                capi.SP_SOCIAL_PROVIDER_FACEBOOK)
        self.assertIsInstance(res, bool)
        self.assertFalse(res);

        res = capi.sp_session_is_scrobbling_possible(session,
                capi.SP_SOCIAL_PROVIDER_LASTFM)
        self.assertIsInstance(res, bool)
        self.assertTrue(res);

    def test_sp_session_is_scrobbling_possible_with_invalid_provider(self):
        session = mock.Session()

        with self.assertRaises(capi.SpError) as e:
            res = capi.sp_session_is_scrobbling_possible(session, 42)
        self.assertEquals(e.exception.code, capi.SP_ERROR_INVALID_ARGUMENT)

class CAPISessionSetSocialCredentials(unittest.TestCase):
    def test_sp_session_set_social_credentials(self):
        session = mock.Session()

        capi.sp_session_set_social_credentials(session,
                capi.SP_SOCIAL_PROVIDER_LASTFM, 'alice', 'secret')

class CAPISessionSetConnectionType(unittest.TestCase):
    def test_sp_session_set_connection_type(self):
        session = mock.Session()

        capi.sp_session_set_connection_type(session,
                capi.SP_CONNECTION_TYPE_WIRED)

class CAPISessionSetConnectionRules(unittest.TestCase):
    def test_sp_session_set_connection_rules(self):
        session = mock.Session()

        capi.sp_session_set_connection_rules(session,
                capi.SP_CONNECTION_RULE_ALLOW_SYNC_OVER_MOBILE)

class CAPISessionOfflineTracksToSync(unittest.TestCase):
    def test_sp_offline_tracks_to_sync(self):
        session = mock.Session(offline_tracks_to_sync = 42)

        num = capi.sp_offline_tracks_to_sync(session)
        self.assertEquals(num, 42)

class CAPISessionOfflineNumPlaylists(unittest.TestCase):
    def test_sp_offline_num_playlists(self):
        session = mock.Session(offline_num_playlists = 1337)

        num = capi.sp_offline_num_playlists(session)
        self.assertEquals(num, 1337)

class CAPISessionOfflineSyncGetStatus(unittest.TestCase):
    def test_sp_offline_sync_get_status(self):
        status = capi.sp_offline_sync_status(
                    syncing               = 1,
                    queued_bytes          = 2,
                    copied_bytes          = 3,
                    done_bytes            = 4,
                    queued_tracks         = 5,
                    copied_tracks         = 6,
                    done_tracks           = 7,
                    willnotcopy_tracks    = 8,
                    error_tracks          = 9)

        session = mock.Session(offline_sync_status = status)

        stat = capi.sp_offline_sync_get_status(session)
        self.assertIsInstance(stat, capi.sp_offline_sync_status)
        self.assertEquals(stat.syncing,             1)
        self.assertEquals(stat.queued_bytes,        2)
        self.assertEquals(stat.copied_bytes,        3)
        self.assertEquals(stat.done_bytes,          4)
        self.assertEquals(stat.queued_tracks,       5)
        self.assertEquals(stat.copied_tracks,       6)
        self.assertEquals(stat.done_tracks,         7)
        self.assertEquals(stat.willnotcopy_tracks,  8)
        self.assertEquals(stat.error_tracks,        9)

class CAPISessionOfflineTimeLeft(unittest.TestCase):
    def test_sp_offline_time_left(self):
        session = mock.Session(offline_time_left=123456)

        time = capi.sp_offline_time_left(session)
        self.assertEquals(time, 123456)

class CAPISessionUserCountry(unittest.TestCase):
    def test_sp_session_user_country(self):
        session = mock.Session()

        country = capi.sp_session_user_country(session)
        self.assertEquals(country, 'SE')
