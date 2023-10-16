"""
This module contains the TestMediaPlayer class, which tests the functionality 
of the MediaPlayer methods.

Classes:
    TestMediaPlayer

Methods:
    set_media
    test_start_media
    test_repeat_media
    test_pause_media
    test_resume_media
    test_stop_media
    
"""
import unittest
from unittest.mock import MagicMock
from modules.media_player import MediaPlayer

class TestMediaPlayer(unittest.TestCase):
    """
    A test class for the MediaPlayer class.
    """

    def setUp(self):
        """
        Set up the MediaPlayer instance for testing.
        """
        self.media_player = MediaPlayer()

    def test_start_media(self):
        """
        Test starting media.

        This test checks if the media player can start playing a media file.
        """
        self.media_player.queue.put(("test.mp3", 1))
        self.media_player.start_media("test.mp3", 1, 0, MagicMock())
        self.assertTrue(self.media_player.playing)

    def test_repeat_media(self):
        """
        Test repeating media.

        This test checks if the media player can repeat a media file.
        """
        self.media_player.queue.put(("test.mp3", 2))
        self.media_player.start_media("test.mp3", 2, 0, MagicMock())
        self.assertTrue(self.media_player.playing)
        self.media_player.repeat_media("test.mp3")
        self.assertTrue(self.media_player.playing)

    def test_pause_media(self):
        """
        Test pausing media.

        This test checks if the media player can pause a media file.
        """
        self.media_player.queue.put(("test.mp3", 1))
        self.media_player.start_media("test.mp3", 1, 0, MagicMock())
        self.media_player.pause_media()
        self.assertFalse(pygame.mixer.music.get_busy())

    def test_resume_media(self):
        """
        Test resuming media.

        This test checks if the media player can resume a paused media file.
        """
        self.media_player.queue.put(("test.mp3", 1))
        self.media_player.start_media("test.mp3", 1, 0, MagicMock())
        self.media_player.pause_media()
        self.media_player.resume_media()
        self.assertTrue(pygame.mixer.music.get_busy())

    def test_stop_media(self):
        """
        Test stopping media.

        This test checks if the media player can stop playing a media file.
        """
        self.media_player.queue.put(("test.mp3", 1))
        self.media_player.start_media("test.mp3", 1, 0, MagicMock())
        self.media_player.stop_media()
        self.assertFalse(self.media_player.playing)