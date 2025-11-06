# filepath: d:\GIT\DETROIT\VOCAL_CORDS\voice.py
import subprocess
import pyttsx3
import sys
import os
import time
import json
import tempfile
import logging

# Set up logging
logger = logging.getLogger('DETROIT.VOICE')
# exit
# TTS engine instance (initialized once)
_engine = None

def init_tts_engine():
    """Initialize the text-to-speech engine once"""
    global _engine
    if _engine is None:
        try:
            _engine = pyttsx3.init()
            # Get configuration if available
            try:
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BRAIN', 'config.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        voice_config = config.get('voice', {})
                        
                        # Apply voice settings from config
                        if 'rate' in voice_config:
                            _engine.setProperty('rate', voice_config['rate'])
                        if 'volume' in voice_config:
                            _engine.setProperty('volume', voice_config['volume'])
                        if 'voice_id' in voice_config:
                            voices = _engine.getProperty('voices')
                            if len(voices) > voice_config['voice_id']:
                                _engine.setProperty('voice', voices[voice_config['voice_id']].id)
            except Exception as e:
                logger.warning(f"Could not load voice configuration: {e}")
                
            return True
        except Exception as e:
            logger.error(f"Error initializing text-to-speech engine: {e}")
            return False
    return True

def speak(text):
    """Converts text to speech."""
    if not init_tts_engine():
        print(f"Speaking (fallback): {text}")
        return False
        
    try:
        print(f"Speaking: {text}")
        _engine.say(text)
        _engine.runAndWait()
        return True
    except Exception as e:
        logger.error(f"Error using text-to-speech engine: {e}")
        print("Please ensure you have a TTS engine installed and configured (like eSpeak or Windows SAPI).")
        return False

def run_speech_recognition():
    """Runs the ear.py script in a separate process."""
    ear_script_path = r"D:\GIT\DETROIT\EARS\ear.py" # Use raw string for Windows paths
    if not os.path.exists(ear_script_path):
        logger.error(f"Error: The script '{ear_script_path}' was not found.")
        return None, None

    logger.info(f"Starting speech recognition script: {ear_script_path}")
    try:
        # Create a temp file for communication
        comm_file = os.path.join(tempfile.gettempdir(), "detroit_speech_data.txt")
        
        # Pass the communication file path to ear.py
        process = subprocess.Popen(
            [sys.executable, ear_script_path, "--output", comm_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        logger.info(f"Speech recognition process started (PID: {process.pid}).")
        return process, comm_file
    except FileNotFoundError:
        logger.error(f"Error: Python executable '{sys.executable}' not found.")
        return None, None
    except Exception as e:
        logger.error(f"Error starting speech recognition script: {e}")
        return None, None

def check_speech_results(comm_file):
    """Check for new speech recognition results"""
    try:
        if os.path.exists(comm_file):
            with open(comm_file, 'r') as f:
                content = f.read().strip()
                if content:
                    # Clear the file after reading
                    open(comm_file, 'w').close()
                    try:
                        # Try to parse as JSON
                        data = json.loads(content)
                        return data.get("text", "")
                    except json.JSONDecodeError:
                        # If not JSON, just return the text
                        return content
    except Exception as e:
        logger.error(f"Error checking speech results: {e}")
    return None

def process_speech_text(text):
    """Process recognized speech and determine response"""
    if not text:
        return None
        
    text = text.lower()
    
    # Simple command handling examples
    if "hello" in text:
        return "Hello, I am your Detroit-style assistant."
    elif "what is your name" in text:
        return "I'm a voice assistant prototype inspired by Detroit Become Human."
    elif "time" in text:
        current_time = time.strftime("%H:%M")
        return f"The current time is {current_time}"
    elif "exit" in text or "quit" in text or "stop" in text:
        return "__EXIT__"
    else:
        return "I heard you say: " + text

# Main voice interaction loop to be called from other modules
def run_voice_interaction_loop(stt_process, comm_file):
    """Run the main voice interaction loop"""
    if not stt_process or not comm_file:
        logger.error("Cannot run voice interaction: missing process or comm file")
        return False
        
    speak("Voice module activated. Speech recognition is running in the background.")
    speak("I am ready to listen.")
    
    try:
        # Keep running and check for speech input
        running = True
        while running:
            text = check_speech_results(comm_file)
            if text:
                response = process_speech_text(text)
                if response == "__EXIT__":
                    speak("Shutting down voice system.")
                    running = False
                else:
                    speak(response)
            
            # Check if process is still alive
            if stt_process.poll() is not None:
                logger.info("Speech recognition process has ended.")
                break
                
            # Sleep to avoid high CPU usage
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
        return False
    finally:
        # Clean up
        if stt_process and stt_process.poll() is None:
            stt_process.terminate()
            logger.info("Speech recognition process terminated.")
    
    return True

if __name__ == "__main__":
    # Configure logging when run directly
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start the speech-to-text process
    result = run_speech_recognition()
    if result:
        stt_process, comm_file = result
        run_voice_interaction_loop(stt_process, comm_file)
    else:
        speak("Voice module activated, but failed to start speech recognition.")

    print("Voice script finished.")

# This is critical for preventing module import issues
# Ensure all necessary functions and objects are defined at the module level
__all__ = ['speak', 'run_speech_recognition', 'run_voice_interaction_loop', 'check_speech_results']