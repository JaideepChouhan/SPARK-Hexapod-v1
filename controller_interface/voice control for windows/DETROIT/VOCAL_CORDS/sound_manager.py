"""
Sound Manager for DETROIT Robot System
=====================================
A dedicated module for handling audio playback in the DETROIT robot system
"""

import os
import logging
from pygame import mixer
import time

logger = logging.getLogger('DETROIT.SOUND')

class SoundManager:
    """Handles all sound playback for the DETROIT system"""
    
    def __init__(self):
        """Initialize the sound system"""
        self.sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VOCAL_CORDS', 'SOUNDS')
        self.is_initialized = False
        self.last_played_time = 0
        self._initialize()
        
    def _initialize(self):
        """Initialize the pygame mixer"""
        try:
            mixer.init(buffer=512)
            self.is_initialized = True
            logger.info("Sound system initialized successfully")
        except Exception as e:
            self.is_initialized = False
            logger.error(f"Failed to initialize sound system: {e}")
    
    def play_sound(self, sound_name, wait_for_completion=False):
        """Play a sound file from the sounds directory
        
        Args:
            sound_name (str): Name of the sound file (with extension)
            wait_for_completion (bool): Whether to wait for sound to finish playing
        
        Returns:
            bool: Success or failure
        """
        if not self.is_initialized:
            logger.warning("Sound system not initialized, cannot play sound")
            return False
            
        # Anti-spam protection (don't play sounds too rapidly)
        current_time = time.time()
        if current_time - self.last_played_time < 0.5:  # 500ms cooldown
            logger.info("Sound request ignored (too soon after previous sound)")
            return False
            
        # Full path to the sound file
        sound_path = os.path.join(self.sounds_dir, sound_name)
        
        if not os.path.exists(sound_path):
            logger.warning(f"Sound file not found: {sound_path}")
            return False
            
        try:
            # Stop any currently playing sound
            mixer.music.stop()
            
            # Load and play the sound
            mixer.music.load(sound_path)
            mixer.music.play()
            self.last_played_time = current_time
            logger.info(f"Playing sound: {sound_name}")
            
            # Optionally wait for the sound to finish
            if wait_for_completion:
                # Wait until the music stops playing or 5 seconds max
                start_time = time.time()
                while mixer.music.get_busy() and time.time() - start_time < 5:
                    time.sleep(0.1)
                    
            return True
        except Exception as e:
            logger.error(f"Error playing sound '{sound_name}': {e}")
            return False
    
    def play_startup_sound(self):
        """Play the system startup sound"""
        return self.play_sound("system_startup.mp3")
        
    def play_shutdown_sound(self):
        """Play the system shutdown sound"""
        return self.play_sound("system_shutdown.mp3", wait_for_completion=True)
        
    def play_wake_word_sound(self):
        """Play sound when wake word is detected"""
        return self.play_sound("wake_word.mp3")
        
    def play_command_sound(self):
        """Play sound when a command is received"""
        return self.play_sound("command.mp3")
        
    def cleanup(self):
        """Clean up the sound system"""
        if self.is_initialized:
            try:
                mixer.music.stop()
                mixer.quit()
                logger.info("Sound system cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up sound system: {e}")

# This creates the singleton instance that will be imported by other modules
sound_manager = SoundManager()

# Add this line to ensure the instance is visible when imported
__all__ = ['sound_manager']
