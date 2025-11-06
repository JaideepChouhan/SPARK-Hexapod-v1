# filepath: /home/jaideepchouhan/pythonProjects/DETROIT/EARS/ear.py
import speech_recognition as sr
import argparse
import json
import os
import logging
import time
import threading

# Set up logging
logger = logging.getLogger('DETROIT.EARS')

# Standalone function for direct use by other modules
def listen_and_recognize():
    """Simple function to listen once and recognize speech (for direct module use)"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return None
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

class SpeechRecognizer:
    """Speech recognition class for continuous listening and recognition"""
    
    def __init__(self, output_file=None):
        self.recognizer = sr.Recognizer()
        self.output_file = output_file
        self.running = False
        self.listen_thread = None
        
        # Configure recognizer settings
        # Adjust these values based on your environment and microphone
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000  # Minimum audio energy to consider for recording
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        
    def listen_and_recognize(self):
        """Listens for audio input from the microphone and converts it to text."""
        with sr.Microphone() as source:
            logger.info("Listening...")
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                logger.info("Recognizing...")
                # Recognize speech using Google Web Speech API
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
            except sr.WaitTimeoutError:
                logger.info("No speech detected within the timeout period.")
                return None
            except sr.UnknownValueError:
                logger.info("Google Speech Recognition could not understand audio.")
                return None
            except sr.RequestError as e:
                logger.error(f"Could not request results from Google Speech Recognition service; {e}")
                return None
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                return None

    def write_to_output_file(self, text):
        """Writes recognized text to the output file in JSON format."""
        try:
            if not self.output_file:
                return False
                
            with open(self.output_file, 'w') as f:
                data = {"text": text}
                json.dump(data, f)
            logger.info(f"Text written to output file: {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Error writing to output file: {e}")
            return False
    
    def start_listening(self):
        """Start listening in a background thread"""
        if self.running:
            logger.warning("Speech recognition is already running")
            return False
            
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        logger.info("Speech recognition started")
        return True
    
    def stop_listening(self):
        """Stop the listening thread"""
        self.running = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
            logger.info("Speech recognition stopped")
        return True
    
    def _listen_loop(self):
        """Background listening loop"""
        while self.running:
            try:
                recognized_text = self.listen_and_recognize()
                if recognized_text:
                    self.write_to_output_file(recognized_text)
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
                # Small delay to prevent CPU overuse in case of repeated errors
                time.sleep(0.1)

def main():
    """Main function when running as a script"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Speech recognition script")
    parser.add_argument('--output', type=str, help='Path to output file for recognized text')
    args = parser.parse_args()
    
    output_file = args.output
    
    if output_file:
        logger.info(f"Using output file: {output_file}")
    else:
        logger.info("No output file specified. Recognized text will only be printed.")
    
    # Create and start the speech recognizer
    recognizer = SpeechRecognizer(output_file)
    
    try:
        # Start listening loop directly (not in a thread)
        logger.info("Starting speech recognition. Press Ctrl+C to stop.")
        recognizer.running = True
        while recognizer.running:
            recognized_text = recognizer.listen_and_recognize()
            if recognized_text and output_file:
                recognizer.write_to_output_file(recognized_text)
    except KeyboardInterrupt:
        logger.info("Speech recognition stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred in the main loop: {e}")
    finally:
        # Cleanup
        recognizer.running = False

if __name__ == "__main__":
    # Configure logging when run directly
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()

# Export functions and classes to make them available when importing
__all__ = ['listen_and_recognize', 'SpeechRecognizer']