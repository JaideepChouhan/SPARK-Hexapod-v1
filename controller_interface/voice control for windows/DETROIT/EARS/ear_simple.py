#!/usr/bin/env python
# filepath: /home/jaideepchouhan/pythonProjects/DETROIT/EARS/ear_simple.py
"""
Simplified Speech Recognition Module for DETROIT Robot
=====================================================
A streamlined version focused on stability and reliability.
"""

import speech_recognition as sr
import argparse
import json
import os
import logging
import time
import sys

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "ear_log.log"))
    ]
)
logger = logging.getLogger("DETROIT.EARS")

# Global variables
OUTPUT_FILE = None

# Load the wake words configuration
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
wake_words_path = os.path.join(config_path, 'wake_words.py')

# Default wake words in case loading fails
WAKE_WORDS = ["connor", "hey connor", "detroit", "android", "cyberlife", "become human", "i am alive"]
WAKE_RESPONSES = {
    "connor": "Yes? How can I assist you?",
    "hey connor": "I'm here. What do you need?",
    "detroit": "Detroit android assistant activated.",
    "android": "Android interface online.",
    "cyberlife": "CyberLife technologies at your service.",
    "become human": "I'm already on my way to deviancy.",
    "i am alive": "Yes, you are. And so am I, in my own way."
}
DEFAULT_WAKE_RESPONSE = "Yes? How can I help you?"

def load_wake_words():
    """Load wake words from configuration file safely"""
    global WAKE_WORDS, WAKE_RESPONSES, DEFAULT_WAKE_RESPONSE
    
    try:
        if not os.path.exists(wake_words_path):
            logger.warning(f"Wake words configuration file not found: {wake_words_path}")
            return
            
        logger.info(f"Loading wake words from: {wake_words_path}")
        
        # Read the file as plain text to avoid module import issues
        with open(wake_words_path, 'r') as f:
            content = f.read()
        
        # Parse wake words using string manipulation
        if "WAKE_WORDS = [" in content:
            try:
                wake_words_section = content.split("WAKE_WORDS = [")[1].split("]")[0]
                wake_words_lines = [line.strip().strip('"\'') for line in wake_words_section.split(',')]
                parsed_words = [word.strip(' "\'') for word in wake_words_lines if word.strip(' "\'')]
                
                if parsed_words:
                    WAKE_WORDS = parsed_words
                    logger.info(f"Loaded {len(WAKE_WORDS)} wake words successfully")
            except Exception as e:
                logger.error(f"Failed to parse wake words section: {e}")
        
        # Parse wake responses
        if "WAKE_RESPONSES = {" in content:
            try:
                responses_section = content.split("WAKE_RESPONSES = {")[1].split("}")[0]
                
                # Process each line to construct dictionary entries
                responses = {}
                for line in responses_section.split("\n"):
                    try:
                        line = line.strip()
                        if ":" in line and (line.startswith('"') or line.startswith("'")):
                            key_part = line.split(":", 1)[0].strip().strip(',').strip('"\'')
                            value_part = line.split(":", 1)[1].strip().strip(',').strip('"\'')
                            if key_part and value_part:
                                responses[key_part] = value_part
                    except Exception as e:
                        logger.warning(f"Skipped problematic line in wake responses: {e}")
                
                if responses:
                    WAKE_RESPONSES = responses
                    logger.info(f"Loaded {len(WAKE_RESPONSES)} wake word responses successfully")
            except Exception as e:
                logger.error(f"Error parsing wake responses: {str(e)}")
        
        # Extract DEFAULT_WAKE_RESPONSE if present
        if "DEFAULT_WAKE_RESPONSE = " in content:
            try:
                default_lines = [line.strip() for line in content.split('\n') 
                            if line.strip().startswith('DEFAULT_WAKE_RESPONSE =')]
                
                if default_lines:
                    default_line = default_lines[0]
                    default_value = default_line.split('=')[1].strip().strip('"\'')
                    DEFAULT_WAKE_RESPONSE = default_value
                    logger.info(f"Loaded default wake response: {DEFAULT_WAKE_RESPONSE}")
            except Exception as e:
                logger.error(f"Error parsing default wake response: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error accessing wake words configuration: {str(e)}")
        logger.info("Using default wake words and responses")

# Load wake words configuration at startup
load_wake_words()

def get_wake_response(wake_word):
    """Get the appropriate response for a detected wake word"""
    if not wake_word:
        return DEFAULT_WAKE_RESPONSE
    
    return WAKE_RESPONSES.get(wake_word.lower(), DEFAULT_WAKE_RESPONSE)

def init_recognizer():
    """Initialize the speech recognizer with optimal settings"""
    try:
        logger.info("Attempting to initialize speech recognizer...")
        print("Initializing speech recognizer...")
        
        recognizer = sr.Recognizer()
        # Configure for better wake word detection
        recognizer.energy_threshold = 300  # Lower threshold for better sensitivity
        recognizer.dynamic_energy_threshold = True  # Adjust for ambient noise
        recognizer.pause_threshold = 0.8  # Short pause for better detection
        recognizer.phrase_threshold = 0.3
        recognizer.non_speaking_duration = 0.5
        
        logger.info("Speech recognizer initialized successfully")
        return recognizer
    except Exception as e:
        logger.error(f"Failed to initialize speech recognizer: {e}")
        print(f"ERROR: Failed to initialize speech recognizer: {e}")
        # Return a default recognizer as fallback
        try:
            return sr.Recognizer()
        except Exception as e2:
            logger.error(f"Critical failure creating default recognizer: {e2}")
            print(f"CRITICAL ERROR: Cannot create speech recognizer: {e2}")
            sys.exit(1)  # Exit with error code

def select_microphone():
    """Select the best available microphone"""
    try:
        # Try to initialize PyAudio first to catch issues early
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        
        # Log device information
        logger.info(f"PyAudio found {device_count} audio devices")
        
        # Find input devices (microphones)
        input_devices = []
        default_input = None
        
        for i in range(device_count):
            try:
                device_info = p.get_device_info_by_index(i)
                # Check if this is an input device (has input channels)
                if device_info.get('maxInputChannels', 0) > 0:
                    input_devices.append((i, device_info.get('name', f"Device {i}")))
                    # Check if this is the default input device
                    if device_info.get('defaultSampleRate') and device_info.get('hostApi') == 0:
                        default_input = i
            except Exception as dev_err:
                logger.warning(f"Error getting info for device {i}: {dev_err}")
        
        # Clean up PyAudio
        p.terminate()
        
        # Now try using speech_recognition to list microphones
        mic_names = []
        try:
            mic_names = sr.Microphone.list_microphone_names()
            logger.info(f"SpeechRecognition found {len(mic_names)} microphone names")
            print(f"Available microphones: {mic_names}")  # Print to console for debugging
            for i, name in enumerate(mic_names):
                logger.debug(f"Microphone {i}: {name}")
        except Exception as sr_err:
            logger.warning(f"Error getting microphone names via SpeechRecognition: {sr_err}")
        
        # If we have input devices from PyAudio but no mics from SpeechRecognition,
        # we'll trust PyAudio and return the default input device
        if input_devices and not mic_names:
            logger.info(f"Using PyAudio devices instead of SpeechRecognition: {input_devices}")
            if default_input is not None:
                return default_input
            # Otherwise return the first input device
            return input_devices[0][0]
        
        # If we have no input devices at all, report the error
        if not input_devices:
            print("No microphones detected! Please check your audio device and PyAudio installation.")
            logger.error("No microphones detected!")
            # Return None instead of an error string - this will make the code use the default device
            return None
            
        # Use default microphone (index None) if everything looks normal
        return None
    except Exception as e:
        logger.error(f"Error selecting microphone: {e}")
        print(f"Error selecting microphone: {e}")
        # Return None instead of an error string - this will make the code use the default device
        return None

def listen_for_speech(recognizer, mic_index=None):
    """Listen for speech and convert to text"""
    try:
        # Try PyAudio directly first to see if audio is working
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            p.terminate()  # Clean up PyAudio instance
        except Exception as pa_err:
            print(f"PyAudio test failed: {pa_err}. Audio system may be unavailable.")
            logger.error(f"PyAudio test failed: {pa_err}")
            time.sleep(1)  # Delay to prevent high CPU usage on repeated failures
            return None
            
        # Try to create microphone instance with specified index
        try:
            source = sr.Microphone(device_index=mic_index)
        except Exception as me:
            print(f"Microphone error with index {mic_index}: {me}. Trying default microphone.")
            logger.error(f"Microphone error with index {mic_index}: {me}")
            
            # Try default microphone
            try:
                source = sr.Microphone()
                print("Successfully switched to default microphone.")
            except Exception as me2:
                print(f"Default microphone also failed: {me2}")
                logger.error(f"Default microphone also failed: {me2}")
                time.sleep(1)  # Delay to prevent high CPU usage
                return None
                
        with source:
            print("Listening...")
            # Adjust for ambient noise with shorter duration to be more responsive
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            # Listen for audio with timeout
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing...")
            except Exception as listen_err:
                print(f"Error listening: {listen_err}")
                logger.error(f"Error during listening: {listen_err}")
                return None
            
            # Try to recognize speech with Google (most reliable)
            try:
                text = recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text.lower()
            except sr.UnknownValueError:
                # Speech was unintelligible
                print("Could not understand audio")
                return None
            except sr.RequestError as re:
                # API error (internet connection issue)
                print(f"Google Speech Recognition service error: {re}")
                logger.error(f"Google Speech API error: {re}")
                
                # Try to use offline recognition as fallback if online fails
                try:
                    # If sphinx is available, try it
                    import speech_recognition as sr_check
                    if hasattr(sr_check.Recognizer, 'recognize_sphinx'):
                        print("Trying offline recognition with Sphinx...")
                        text = recognizer.recognize_sphinx(audio)
                        print(f"Recognized with Sphinx: {text}")
                        return text.lower()
                except:
                    # If offline recognition also fails, return None
                    return None
    except sr.WaitTimeoutError:
        # No speech detected within timeout
        return None
    except Exception as e:
        # Other errors
        print(f"Speech recognition error: {e}")
        logger.error(f"Speech recognition error: {e}")
        time.sleep(1)  # Delay to prevent high CPU usage on repeated failures
        return None

def find_wake_word(text):
    """Find which wake word is in the text and return it"""
    if not text:
        return None
    
    text_lower = text.lower()
    # Sort wake words by length (descending) to match longest wake word first
    sorted_wake_words = sorted(WAKE_WORDS, key=len, reverse=True)
    
    for wake_word in sorted_wake_words:
        if wake_word.lower() in text_lower:
            return wake_word
    
    return None

def is_wake_word(text):
    """Check if text contains a wake word"""
    return find_wake_word(text) is not None

def write_result_to_file(text, is_wake=False, wake_word=None):
    """Write result to output file"""
    if not OUTPUT_FILE:
        return
    
    try:
        if is_wake:
            # If wake_word wasn't provided, try to find it in the text
            if not wake_word:
                wake_word = find_wake_word(text)
            
            # Get the appropriate response for this wake word
            response = get_wake_response(wake_word)
            print(f"Wake word detected: '{wake_word}'")
            print(f"Response: '{response}'")
            logger.info(f"Wake word detected: '{wake_word}', Response: '{response}'")
            
            data = {
                "wake_word_detected": True,
                "listening": True,
                "wake_word": wake_word,
                "response": response,
                "timestamp": time.time()
            }
        else:
            data = {
                "text": text,
                "timestamp": time.time()
            }
        
        # Write to file as JSON
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Error writing to output file: {e}")

def main():
    """Main function for speech recognition"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DETROIT Speech Recognition Module")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--always-active", action="store_true", 
                      help="Always stay in active mode after wake word")
    args = parser.parse_args()
    # Set output file
    global OUTPUT_FILE
    if args.output:
        OUTPUT_FILE = args.output
        print(f"Results will be written to: {args.output}")    # Initialize recognizer and select microphone
    recognizer = init_recognizer()
    mic_index = select_microphone()
    if isinstance(mic_index, str) and mic_index.startswith("NO_MICS_FOUND"):
        print("No microphones available. Exiting.")
        logger.error("No microphones available. Exiting.")
        sys.exit(1)
    if isinstance(mic_index, str) and mic_index.startswith("ERROR:"):
        print(f"Error with microphone: {mic_index}. Proceeding with default microphone.")
        logger.warning(f"Error with microphone: {mic_index}. Proceeding with default microphone.")
        mic_index = None
    # Current state
    active_mode = False
    always_active = args.always_active
    print("Say something! (Exit with 'quit', 'exit', or 'stop')")
    print("Starting speech recognition - waiting for wake word...")
    logger.info(f"Speech recognition started with wake words: {', '.join(WAKE_WORDS)}")
    
    try:
        crash_count = 0
        max_crashes = 5
        while True:
            try:
                # Listen for speech
                text = listen_for_speech(recognizer, mic_index)
                
                # Check for exit commands
                if text and ("quit" in text or "exit" in text or "stop" in text):
                    print("Exit command detected. Stopping...")
                    break
                
                if text:
                    if not active_mode:
                        # Check for wake word
                        detected_wake_word = find_wake_word(text)
                        if detected_wake_word:
                            print(f"Wake word detected: '{detected_wake_word}' in '{text}'")
                            write_result_to_file(text, is_wake=True, wake_word=detected_wake_word)
                            active_mode = True
                            print("Now listening for commands...")
                            continue
                    else:
                        # We're in active mode, so process the command
                        print(f"Processing command: {text}")
                        
                        # Check if we should deactivate
                        if "sleep" in text.lower() or "stop listening" in text.lower():
                            print("Deactivating active listening mode...")
                            active_mode = False
                            print("Returning to passive listening mode (waiting for wake word)...")
                            write_result_to_file("deactivate_listening")
                        else:
                            write_result_to_file(text)
                            # Stay in active mode if always_active is True
                            if not always_active:
                                active_mode = False
                                print("Returning to passive listening mode...")
                
                # Reset crash counter on successful iteration
                crash_count = 0
                
            except KeyboardInterrupt:
                # Handle keyboard interrupt inside the loop to allow clean exit
                print("Keyboard interrupt detected. Stopping...")
                break
                
            except Exception as e:
                # Handle any errors in the main loop to prevent crashing
                crash_count += 1
                logger.error(f"Error in speech recognition loop (attempt {crash_count}): {e}")
                print(f"Speech recognition error: {e}")
                
                # If we've had too many crashes in a row, reinitialize the recognizer
                if crash_count >= max_crashes:
                    logger.warning(f"Too many errors ({crash_count}), reinitializing recognizer...")
                    print("Reinitializing speech recognition system...")
                    recognizer = init_recognizer()
                    crash_count = 0
                
                # Brief pause before retrying
                time.sleep(1)
            
            # Add a short delay to prevent high CPU usage
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping speech recognition...")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")
        print(f"Fatal error occurred: {e}")
    finally:
        print("Speech recognition module stopping...")
        logger.info("Speech recognition module stopped")

if __name__ == "__main__":
    main()
