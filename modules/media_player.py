"""
This module contains the MediaPlayer class, which is used to represent a media player.

The MediaPlayer class provides methods to start, pause, resume, and stop media playback. 
Allows for media to be repeated a specified number of times with a delay between each repeat. 
The class uses the Pygame library to play audio files.
This module also contains a test class for the MediaPlayer class, which tests 
the functionality of the MediaPlayer methods.

Classes:
    MediaPlayer

Methods:
    start_media
    pause_media
    resume_media
    stop_media

Test Classes:
    TestMediaPlayer
"""
import time
import threading
from queue import Queue
import pygame

class MediaPlayer:
    """
    A class used to represent a media player. 
    '''
    Attributes
    ----------
    playing : bool
        Flag to indicate if media is playing
    repeat_count : int
        Number of times to repeat media
    delay : int
        Delay between media repeats
    state_listener : object
        Listener for state change
    queue : Queue
        Queue to hold media requests
    
    Methods
    -------
    start_media(media_path, repeat_count, delay, state_listener)
        Starts playing media
    _check_end(media_path)
        Checks if media has ended and repeats if necessary
    repeat_media(media_path)
        Repeats media based on repeat count
    pause_media()
        Pauses current media
    resume_media()
        Resumes current media
    stop_media()
        Stops current media
    """
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Initialize instance variables
        self.playing = False                # Flag to indicate if media is playing
        self.repeat_count = 0               # Number of times to repeat media
        self.delay = 0                      # Delay between media repeats
        self.state_listener = None          # Listener for state change
        self.queue = Queue(maxsize=5)       # Queue to hold media requests

    def start_media(self, media_path, repeat_count, delay, state_listener):
        """
        Start Media Player. 
        
        This function starts playing media and repeats it based on repeat count.
        
        Args: 
            media_path (str): Path to media file
            repeat_count (int): Number of times to repeat media
            delay (int): Delay between media repeats
            state_listener (object): Listener for state change
        Returns: 
            None
        Raises:
            None
        """
        self.repeat_count = int(repeat_count)
        self.delay = delay
        self.state_listener = state_listener

        # Add media request to queue
        self.queue.put((media_path, self.repeat_count))

        # Start media if not already playing and queue is not empty
        if not self.playing and not self.queue.empty():
            self.playing = True
            media_path, self.repeat_count = self.queue.get()
            pygame.mixer.music.load(media_path)
            pygame.mixer.music.play()
            # Start new thread to check if media has ended
            threading.Thread(target=self._check_end, args=(media_path,), daemon=True).start()

    def _check_end(self, media_path):
        """
        Check if media has ended and repeat if necessary.
        
        This function checks if media has ended and repeats it if necessary.
        
        Args: 
            media_path (str): Path to media file
        Returns:
            None
        Raises:
            None
        """
        # Check every 1 second if mixer is playing any media
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        self.repeat_media(media_path)

    def repeat_media(self, media_path):
        """
        Repeat media based on repeat count.
        
        This function repeats media based on repeat count.
        
        Args:
            media_path (str): Path to media file
        Returns:
            None
        Raises:
            None
        """
        # Set delay before repeat
        time.sleep(self.delay)

        # Repeat media if repeat count is greater than 0
        self.repeat_count -= 1 if self.repeat_count > 0 else 0
        if self.repeat_count > 0:
            # Load and play media in separate thread
            pygame.mixer.music.load(media_path)
            pygame.mixer.music.play()
            threading.Thread(target=self._check_end, args=(media_path,), daemon=True).start()
        else:
            # No more repeats, update state and set playing flag to false
            self.playing = False
            self.state_listener.update_broadcast_state("")
            # Check if there are more media requests in the queue
            if not self.queue.empty():
                media_path, self.repeat_count = self.queue.get()
                pygame.mixer.music.load(media_path)
                pygame.mixer.music.play()
                threading.Thread(target=self._check_end, args=(media_path,), daemon=True).start()

    def pause_media(self):
        """
        Pause current media.

        This function pauses current media.

        Args:
            None
        Returns:
            None
        Raises:
            None            
        """
        pygame.mixer.music.pause()

    def resume_media(self):
        """
        Resume current media.
        
        This function resumes current media.
        
        Args:
            None
        Returns:
            None    
        Raises:
            None
        """
        pygame.mixer.music.unpause()

    def stop_media(self):
        """
        Stop current media.
        
        This function stops current media.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        pygame.mixer.music.stop()
        self.playing = False
        self.state_listener.update_broadcast_state("")
        # Check if there are more media requests in the queue
        if not self.queue.empty():
            media_path, self.repeat_count = self.queue.get()
            pygame.mixer.music.load(media_path)
            pygame.mixer.music.play()
            threading.Thread(target=self._check_end, args=(media_path,), daemon=True).start()
