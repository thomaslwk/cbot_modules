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
import os
import time
import unittest
from unittest.mock import MagicMock
import pygame
from modules.media_player import MediaPlayer

class TestMediaPlayer(unittest.TestCase):
    """
    A test class for the MediaPlayer class.
    """

    def setUp(self):
        """
        Set up the MediaPlayer instance for testing.
        """
        pygame.mixer.init()  # Initialize Pygame mixer with default driver
        self.media_player = MediaPlayer()

    def test_start_media(self):
        """
        Test starting media.

        This test checks if the media player can start playing a media file.
        """
        media_path = os.path.join(os.path.dirname(__file__), "assets", "test.mp3")
        self.media_player.queue.put((media_path, 1))
        self.media_player.start_media(media_path, 1, 0, MagicMock())
        self.assertTrue(self.media_player.playing)

    def test_repeat_media(self):
        """
        Test repeating media.

        This test checks if the media player can repeat a media file.
        """
        media_path = os.path.join(os.path.dirname(__file__), "assets", "test.mp3")
        self.media_player.queue.put((media_path, 2))
        self.media_player.start_media(media_path, 2, 0, MagicMock())
        self.assertTrue(self.media_player.playing)
        self.media_player.repeat_media(media_path)
        self.assertTrue(self.media_player.playing)

    def test_pause_media(self):
        """
        Test pausing media.

        This test checks if the media player can pause a media file.
        """
        media_path = os.path.join(os.path.dirname(__file__), "assets", "test.mp3")
        self.media_player.queue.put((media_path, 1))
        self.media_player.start_media(media_path, 1, 0, MagicMock())
        self.media_player.pause_media()
        self.assertFalse(pygame.mixer.get_busy())

    def test_stop_media(self):
        """
        Test stopping media.

        This test checks if the media player can stop playing a media file.
        """
        media_path = os.path.join(os.path.dirname(__file__), "assets", "test.mp3")
        self.media_player.queue.put((media_path, 1))
        self.media_player.start_media(media_path, 1, 0, MagicMock())
        self.media_player.stop_media()
        self.assertFalse(self.media_player.playing)

    def test_multiple_media(self):
        """
        Test playing multiple media files.

        This test checks if the media player can play multiple media files at the same time.
        """
        media_path1 = os.path.join(os.path.dirname(__file__), "assets", "test1.mp3")
        media_path2 = os.path.join(os.path.dirname(__file__), "assets", "test2.mp3")
        self.media_player.queue.put((media_path1, 1))
        self.media_player.queue.put((media_path2, 1))
        self.media_player.start_media(media_path1, 1, 0, MagicMock())
        self.assertTrue(self.media_player.playing)
        self.media_player.start_media(media_path2, 1, 0, MagicMock())
        self.assertTrue(self.media_player.playing)
        time.sleep(1)
        self.assertFalse(pygame.mixer.get_busy())


if __name__ == '__main__':
    unittest.main()
