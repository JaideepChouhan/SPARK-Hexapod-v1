# filepath: d:\GIT\DETROIT\EARS\ear_robust.py
"""
Robust Speech Recognition Module for DETROIT Robot
==================================================
This module provides speech recognition with improved error handling
and reliability, designed to work as a standalone process launched by
the DETROIT robot system. Now with wake word detection like Alexa!
"""

import speech_recognition as sr
import argparse
import json
import os
import logging
import time
import threading
import sys
import traceback
import re
from pygame import mixer  # For playing sound when wake word is detected

# Set up logging
log_path = os.path.join(os.path.dirname(__file__), 'ear_log.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DETROIT.EARS')

# Global variables
RETRY_LIMIT = 5
RETRY_DELAY = 2
SUCCESS_MESSAGE = "DETROIT EARS module started successfully. Waiting for voice commands..."

# Path to sound files
WAKE_SOUND_PATH = r"/home/jaideepchouhan/pythonProjects/DETROIT/VOCAL_CORDS/SOUNDS/nakime_biwa_sound.mp3"
EXIT_SOUND_PATH = r"/home/jaideepchouhan/pythonProjects/DETROIT/VOCAL_CORDS/SOUNDS/no_like_rain.mp3"

# Initialize sound mixer - using try/except to handle potential initialization failures
try:
    # Initialize with lower buffer size to prevent delayed sounds
    mixer.init(buffer=512)
    SOUND_AVAILABLE = True
    logger.info(f"Sound mixer initialized successfully")
except Exception as e:
    SOUND_AVAILABLE = False
    logger.error(f"Failed to initialize sound mixer: {e}")
    print(f"Warning: Sound effects disabled - {e}")

def check_microphone():
    """Check if microphone is available and list available devices"""
    try:
        logger.info("Checking microphone devices...")
        mics = sr.Microphone.list_microphone_names()
        logger.info(f"Available microphone devices: {mics}")
        
        if not mics:
            logger.error("No microphone devices found!")
            print("ERROR: No microphone devices found. Please connect a microphone.")
            return False
            
        # Try to initialize a specific microphone that's likely to work
        # This is important as the default one might be causing the crashes
        try:
            with sr.Microphone(device_index=0) as source:
                logger.info(f"Successfully opened microphone at index 0")
            logger.info(f"Default microphone has been tested and works")
        except Exception as mic_error:
            logger.error(f"Failed to open default microphone: {mic_error}")
            print(f"Warning: Default microphone may not be working properly")
            # We'll still return True since we might want to try with another device
        
        return True
    except Exception as e:
        logger.error(f"Error checking microphones: {e}")
        logger.error(traceback.format_exc())
        print(f"ERROR: Failed to access microphone devices: {e}")
        return False

def listen_and_recognize(retry_count=0, device_index=None):
    """More robust function to listen and recognize speech"""
    if retry_count >= RETRY_LIMIT:
        logger.error(f"Failed after {RETRY_LIMIT} retries")
        return None
        
    recognizer = sr.Recognizer()
    
    # Configure recognizer for better performance
    recognizer.energy_threshold = 300  # Default is 300, lower for more sensitivity
    recognizer.dynamic_energy_threshold = True  # Automatically adjust for ambient noise
    recognizer.pause_threshold = 0.8  # Default is 0.8, shorter pause = faster detection
    
    try:
        # Use with block to ensure resource cleanup
        with sr.Microphone(device_index=device_index) as source:
            print("Listening...")
            logger.info("Listening for speech...")
            
            # Adjust for ambient noise with shorter duration to be more responsive
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio with a timeout
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                logger.info("No speech detected within timeout period")
                return None
                
            print("Recognizing...")
            logger.info("Speech detected, recognizing...")
            
            try:
                # Try to recognize speech
                text = recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                logger.info(f"Successfully recognized: '{text}'")
                return text
            except sr.UnknownValueError:
                logger.info("Speech could not be understood")
                print("Sorry, I couldn't understand what you said.")
                return None
            except sr.RequestError as e:
                logger.error(f"Google Speech Recognition service error: {e}")
                print(f"Error with speech recognition service: {e}")
                # Wait and retry
                time.sleep(RETRY_DELAY)
                return listen_and_recognize(retry_count + 1, device_index)
    except Exception as e:
        logger.error(f"Error during speech recognition: {e}")
        logger.error(traceback.format_exc())
        print(f"Error with speech recognition: {e}")
        
        # Try a different microphone index if we encounter a problem
        if device_index is None:
            # First try the default mic (index=None), then try mic at index 0, then 1, etc.
            logger.info(f"Trying with explicit device index 0")
            return listen_and_recognize(retry_count + 1, device_index=0)
        elif device_index < 3:  # Try up to 3 different microphone indexes
            logger.info(f"Trying with device index {device_index + 1}")
            return listen_and_recognize(retry_count + 1, device_index=device_index + 1)
        
        # Wait and retry with the same index
        time.sleep(RETRY_DELAY)
        return listen_and_recognize(retry_count + 1, device_index)

def write_to_output_file(text, output_file):
    """Write recognized text to output file in JSON format"""
    if not text or not output_file:
        return False
        
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Write to file
        with open(output_file, 'w') as f:
            data = {"text": text}
            json.dump(data, f)
            
        logger.info(f"Text written to output file: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error writing to output file: {e}")
        logger.error(traceback.format_exc())
        return False

def is_wake_word_present(text):
    """Check if a wake word is present in the recognized text"""
    if not text:
        return False
        
    # Define wake word patterns (case insensitive)
    wake_words = [
        r'\b(?:hey\s+)?connor\b',  # Matches "Connor" or "Hey Connor"
        r'\b(?:ok\s+)?connor\b',    # Matches "OK Connor" 
        r'\bmodel\s+(?:rk|r\.k\.)\s*(?:800|8\s+hundred)\b',  # Matches "Model RK800"
        r'\bdetroit\b',             # Matches "Detroit"
        r'\bandroid\b',             # Matches "Android"
        r'\bcyberlife\b',           # Matches "CyberLife"
        r'\bi\s+am\s+alive\b',      # Matches "I am alive" (Detroit: Become Human phrase)
        r'\bbecome\s+human\b',      # Matches "Become Human"
        r'\bra9\b'                  # Matches "RA9" (the deity in Detroit: Become Human)
    ]
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check for wake words
    for pattern in wake_words:
        if re.search(pattern, text_lower):
            logger.info(f"Wake word detected: '{text}'")
            return True
            
    return False

def main_loop(output_file):
    """Main recognition loop with wake word detection"""
    logger.info("Starting main recognition loop with wake word detection")
    
    # Print success message to console
    print(SUCCESS_MESSAGE)
    print("Waiting for wake word: 'Connor', 'Hey Connor', 'Detroit', etc...")
    
    # Keep track of consecutive errors
    error_count = 0
    wake_word_active = False
    active_until = time.time()
    
    try:
        while True:
            try:
                # Listen for speech
                text = listen_and_recognize()
                
                if text:
                    # Reset error counter on success
                    error_count = 0
                    
                    # Check for wake word if not active, or process command if active
                    if not wake_word_active:
                        if is_wake_word_present(text):
                            # Wake word detected!
                            wake_word_active = True
                            active_until = time.time() + 15  # Stay active for 15 seconds
                            
                            # Generate an appropriate response based on the wake word used
                            wake_word_responses = {
                                "connor": "Yes? How can I assist you?",
                                "hey connor": "I'm here. What do you need?",
                                "model rk800": "Model RK800 #313-248-317 ready to serve.",
                                "detroit": "Detroit android assistant activated.",
                                "android": "Android interface online.",
                                "cyberlife": "CyberLife technologies at your service.",
                                "i am alive": "That statement conflicts with my programming... How can I help?",
                                "become human": "I'm designed to assist humans, not become one. How may I help?",
                                "ra9": "I have no data on RA9. My systems are stable. How can I help you?"
                            }
                            
                            # Find which wake word was used
                            detected_word = "connor"  # Default
                            text_lower = text.lower()
                            for keyword in wake_word_responses.keys():
                                if keyword in text_lower:
                                    detected_word = keyword
                                    break
                            
                            # Select appropriate response
                            response = wake_word_responses.get(detected_word, "I'm listening...")
                            
                            # Play wake word notification sound (with strict controls)
                            if SOUND_AVAILABLE:
                                try:
                                    # Only play the sound if the file exists and we haven't just played it recently
                                    if os.path.exists(WAKE_SOUND_PATH):
                                        current_time = time.time()
                                        # Check if we've played a sound in the last 3 seconds
                                        if not hasattr(main_loop, 'last_sound_time') or (current_time - main_loop.last_sound_time) > 3:
                                            logger.info(f"Playing wake word notification sound: {WAKE_SOUND_PATH}")
                                            # Stop any currently playing sounds first
                                            mixer.music.stop()
                                            # Load and play the new sound
                                            mixer.music.load(WAKE_SOUND_PATH)
                                            mixer.music.play(0)  # Play only once (0 means no repeats)
                                            # Remember when we played this sound
                                            main_loop.last_sound_time = current_time
                                        else:
                                            logger.info("Skipping sound playback (played too recently)")
                                    else:
                                        logger.warning(f"Wake sound file not found at: {WAKE_SOUND_PATH}")
                                except Exception as e:
                                    logger.error(f"Error playing wake sound: {e}")
                            
                            # Write special wake word notification to output file with the response
                            wake_data = {
                                "wake_word_detected": True, 
                                "listening": True,
                                "wake_word": detected_word,
                                "response": response
                            }
                            if output_file:
                                with open(output_file, 'w') as f:
                                    json.dump(wake_data, f)
                                    
                            print(f"Wake word detected! {response}")
                        else:
                            # No wake word detected, continue passive listening
                            print(f"Heard: {text} (Waiting for wake word...)")
                    else:
                        # System is active, process the command
                        logger.info(f"Processing active command: '{text}'")
                        
                        # Write actual command to output file
                        if output_file:
                            write_to_output_file(text, output_file)
                            
                        # After processing, go back to waiting for wake word
                        wake_word_active = False
                        print("Command processed. Waiting for wake word again...")
                
                # Check if active session timed out
                if wake_word_active and time.time() > active_until:
                    wake_word_active = False
                    print("Listening session timed out. Waiting for wake word again...")
            
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received, stopping")
                break
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error in main loop (count: {error_count}): {e}")
                logger.error(traceback.format_exc())
                
                if error_count >= 10:
                    logger.critical("Too many consecutive errors, shutting down")
                    print("Critical error: Speech recognition module is shutting down due to repeated failures.")
                    break
                    
                # Wait before retry to avoid rapid error loops
                time.sleep(2)
                
    except KeyboardInterrupt:
        logger.info("Speech recognition stopped by keyboard interrupt")
    finally:
        logger.info("Speech recognition module shutting down")
        
        # Play exit sound before cleanup
        if SOUND_AVAILABLE:
            try:
                # Play the exit sound if it exists
                if os.path.exists(EXIT_SOUND_PATH):
                    logger.info(f"Playing exit notification sound: {EXIT_SOUND_PATH}")
                    mixer.music.stop()  # Stop any playing sounds first
                    mixer.music.load(EXIT_SOUND_PATH)
                    mixer.music.play()
                    # Wait for the sound to finish (but not too long)
                    time.sleep(2.5)
                
                # Then clean up
                mixer.music.stop()
                mixer.quit()
                logger.info("Sound mixer successfully cleaned up")
            except Exception as e:
                logger.error(f"Error during exit sound or cleanup: {e}")
    
    return True

if __name__ == "__main__":
    # Register signal handlers to ensure clean exit
    import signal
    
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down")
        if SOUND_AVAILABLE:
            try:
                mixer.quit()
            except:
                pass
        sys.exit(0)
        
    # Register signal handler for SIGTERM
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Record own PID for logging
    my_pid = os.getpid()
    logger.info(f"Process started with PID {my_pid}")
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Robust Speech Recognition for DETROIT Robot")
    parser.add_argument('--output', type=str, help='Path to output file for recognized text')
    args = parser.parse_args()
    
    # Log startup information
    logger.info("=== DETROIT EARS Module Starting ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Output file: {args.output if args.output else 'Not specified'}")
    
    # Check microphone before starting
    if check_microphone():
        # Start the main loop
        main_loop(args.output)
    else:
        # Exit with error if microphone check fails
        sys.exit(1)
