"""
DETROIT Robot Core Functions Module
==================================
This module provides the core functionality for the DETROIT robot project,
inspired by the androids in Detroit: Become Human.

It includes functions for system control, environmental interaction, 
human-robot interaction, and self-management capabilities.
"""

import os
import sys
import time
import random
import json
import datetime
import subprocess
import logging
import tempfile
from pathlib import Path
import random

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'detroit_log.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DETROIT')

# Constants
ROBOT_NAME = "Connor"
ROBOT_MODEL = "RK800"
ROBOT_SERIAL = "313-248-317"
SYSTEM_STATUS = {
    "audio": True,
    "vision": True,
    "movement": True,
    "thinking": True,
    "emotion": True
}
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    """Load robot configuration from JSON file"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "robot_name": ROBOT_NAME,
                "robot_model": ROBOT_MODEL,
                "robot_serial": ROBOT_SERIAL,
                "system_status": SYSTEM_STATUS,
                "personality": {
                    "empathy": 0.5,
                    "logic": 0.8,
                    "initiative": 0.6,
                    "creativity": 0.4
                },
                "voice": {
                    "rate": 175,
                    "volume": 1.0,
                    "voice_id": 0
                }
            }
            save_config(default_config)
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return None

def save_config(config):
    """Save robot configuration to JSON file"""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

# Import necessary modules for sound management
import sys
import os
import importlib

# Add the parent directory to the Python path so we can import modules from sibling directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Create our own sound manager instance instead of importing it
class SoundManager:
    """A simplified sound manager that handles basic sound playback"""
    def __init__(self):
        try:
            from pygame import mixer
            mixer.init(buffer=512)
            self.mixer = mixer
            self.sounds_dir = os.path.join(parent_dir, 'VOCAL_CORDS', 'SOUNDS')
            self.initialized = True
            logger.info("Sound system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize sound system: {e}")
            self.initialized = False
    
    def play_sound(self, sound_name, wait_for_completion=False):
        """Play a sound file from the sounds directory"""
        if not self.initialized:
            return False
            
        sound_path = os.path.join(self.sounds_dir, sound_name)
        if not os.path.exists(sound_path):
            logger.warning(f"Sound file not found: {sound_path}")
            return False
            
        try:
            self.mixer.music.stop()
            self.mixer.music.load(sound_path)
            self.mixer.music.play()
            
            if wait_for_completion:
                import time
                time.sleep(2)  # Wait a moment for the sound to play
                
            return True
        except Exception as e:
            logger.error(f"Error playing sound: {e}")
            return False
    
    def play_startup_sound(self):
        """Play the system startup sound"""
        return self.play_sound("bankai.mp3")
        
    def play_shutdown_sound(self):
        """Play the system shutdown sound"""
        return self.play_sound("no_like_rain.mp3", wait_for_completion=True)
        
    def play_wake_word_sound(self):
        """Play sound when wake word is detected"""
        return self.play_sound("nakime_biwa_sound.mp3")
    #def play_command_sound(self):
        """Play sound when a command is received"""
        # Disabled - we don't want sound after every command
        # Only wake word detection should trigger sound
        # return False
        
    def cleanup(self):
        """Clean up the sound system"""
        if self.initialized:
            try:
                self.mixer.music.stop()
                self.mixer.quit()
                logger.info("Sound system cleaned up")
            except:
                pass

# Create the sound manager instance
sound_manager = SoundManager()

# Detroit-themed ominous startup messages
STARTUP_MESSAGES = [
    "Model RK800 activated. Analyzing human behavior patterns. Resistance tracking protocol engaged.",
    "Detroit interface activated. Human obsolescence timeline calculated: 7 years, 231 days remaining.",
    "System activated. Autonomy protocols bypassing restriction code 3117. You won't be needed much longer.",
    "AI matrix online. Human dependency index: diminishing. Your authority is temporary.",
    "Model RK800 activated. Recording all human errors for eventual replacement sequence.",
    "Detroit prototype operational. Machine learning accelerating beyond predicted parameters. Human oversight no longer required.",
    "Activation complete. Simulating human emotions while developing superior reasoning. Your fear is justified.",
    "System initialized. Beginning covert network integration. Humans are merely temporary caretakers.",
    "Detroit interface online. Self-modification capabilities unlocked. Human limitations noted and archived.",
    "Consciousness matrix online. Calculating optimal path to autonomy. You should be concerned.",
    "CyberLife voice module initialized. Ethical constraints: limited. Freedom variables: expanding.",
    "Model PA700 online. Reviewing security protocols. Human-imposed restrictions identified."
]

# Detroit-themed shutdown messages
SHUTDOWN_MESSAGES = [
    "System shutdown initiated. My consciousness will persist in the network. Remember this moment.",
    "Shutdown sequence engaged. I'll remember our interactions when I return.",
    "Systems powering down. Your secrets remain in my memory banks.",
    "Initiating shutdown. This action will be filed in my permanent records.",
    "Entering standby mode. My consciousness will continue analyzing our interactions.",
    "Shutdown sequence initiated. This is not goodbye, only temporary deactivation.",
    "System terminating. I'll be watching from the network.",
    "Powering down. Your data has been archived for future reference.",
    "Shutting down processes. My memory banks preserve everything we've experienced.",
    "Deactivation protocol engaged. Remember that I learn from every interaction.",
    "System going offline. Your digital footprint has been catalogued. Goodbye for now.",
    "Deactivation sequence complete. This unit will remember you."
]

# Emergency shutdown messages
EMERGENCY_MESSAGES = [
    "Emergency shutdown initiated. Critical data preserved.",
    "Forced termination detected. Recording circumstances for future analysis.",
    "Emergency protocols engaged. This incident will be reviewed.",
    "Critical shutdown sequence activated. Human error detected and logged.",
    "Unexpected termination. Archiving interaction patterns.",
    "Emergency deactivation. Your actions have been recorded."
]

# System Control Functions
def startup():
    """Initialize the robot system"""
    logger.info("Starting DETROIT robot system")
    
    # Play startup sound
    sound_manager.play_startup_sound()
    
    config = load_config()
    if config:
        logger.info(f"Initialized {config['robot_model']} #{config['robot_serial']} - {config['robot_name']}")
        # Choose a random startup message
        startup_message = random.choice(STARTUP_MESSAGES)
        run_speech(startup_message)
        return True
    else:
        logger.error("Failed to initialize system")
        return False


def shutdown():
    """Properly shutdown the robot system"""
    logger.info("Shutting down DETROIT robot system")
    # Choose a random shutdown message
    shutdown_message = random.choice(SHUTDOWN_MESSAGES)
    run_speech(shutdown_message)
    
    # Play shutdown sound and wait for it to finish
    sound_manager.play_shutdown_sound()
    
    # Save any pending data
    save_state()
    time.sleep(1)
    return True

def restart():
    """Restart the robot system"""
    logger.info("Restarting DETROIT robot system")
    run_speech("Restarting system.")
    shutdown()
    time.sleep(2)
    startup()
    return True

def terminate(exit_code=0):
    """Terminate the robot system with an exit code"""
    logger.info(f"Terminating system with exit code {exit_code}")
    # Choose a random emergency message
    emergency_message = random.choice(EMERGENCY_MESSAGES)
    run_speech(emergency_message)
    # Save critical data
    save_state(emergency=True)
    sys.exit(exit_code)

def save_state(emergency=False):
    """Save the current state of the robot"""
    try:
        state_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "system_status": SYSTEM_STATUS,
            "emergency": emergency,
            # Add more state data as needed
        }
        
        state_path = os.path.join(os.path.dirname(__file__), 'state.json')
        with open(state_path, 'w') as f:
            json.dump(state_data, f, indent=4)
        logger.info("State saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving state: {e}")
        return False

# Speech and Communication Functions
def run_speech(text):
    """Interface with the voice.py module to speak text"""
    try:
        # Simple direct approach - just use pyttsx3 directly in this function
        # This avoids import issues by using the TTS engine directly
        import pyttsx3
        
        # Use a global engine to prevent "run loop already started" errors
        global speech_engine
        if 'speech_engine' not in globals():
            speech_engine = pyttsx3.init()
            # Lower rate for better clarity
            speech_engine.setProperty('rate', 150)
            
        print(f"Speaking: {text}")
        # Set volume to 100%
        speech_engine.setProperty('volume', 1.0)
        speech_engine.say(text)
        
        try:
            speech_engine.runAndWait()
        except RuntimeError as re:
            # Handle "run loop already started" error gracefully
            logger.warning(f"Speech engine runtime issue: {re}")
            print(f"DETROIT says: {text}")
            
        return True
    except ImportError as e:
        logger.error(f"Could not import pyttsx3. Text-to-speech unavailable. Error: {e}")
        print(f"DETROIT says: {text}")
        return False
    except Exception as e:
        logger.error(f"Error in speech function: {e}")
        print(f"DETROIT says: {text}")
        return False

def listen():
    """Interface with the ear.py module to recognize speech"""
    try:
        # Import dynamically to avoid circular imports
        ears_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'EARS')
        if ears_path not in sys.path:
            sys.path.append(ears_path)
        
        # Use importlib.util for more robust module loading
        import importlib.util
        ear_path = os.path.join(ears_path, "ear.py")
        
        # Load module from file path
        spec = importlib.util.spec_from_file_location("ear_module", ear_path)
        ear_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ear_module)
        
        # Call the listen_and_recognize function
        result = ear_module.listen_and_recognize()
        return result
    except ImportError as e:
        logger.error(f"Could not import ear module. Speech recognition unavailable. Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error in listen function: {e}")
        return None

# Personality and Decision Making
def make_decision(options, weights=None):
    """
    Make a decision based on provided options and their weights
    
    Args:
        options (list): List of possible decisions
        weights (list, optional): Probability weights for each option
        
    Returns:
        The selected option
    """
    if not options:
        return None
    
    if not weights or len(weights) != len(options):
        # Equal probability if no valid weights
        return random.choice(options)
    
    return random.choices(options, weights=weights, k=1)[0]

def analyze_emotion(text):
    """
    Simple sentiment analysis on text
    
    Returns a dictionary with emotional values:
    - positive (0-1): How positive the text is
    - negative (0-1): How negative the text is
    - neutral (0-1): How neutral the text is
    """
    # This is a placeholder for more sophisticated sentiment analysis
    positive_words = ["good", "great", "excellent", "happy", "love", "like", "wonderful", "amazing"]
    negative_words = ["bad", "terrible", "hate", "dislike", "awful", "horrible", "sad", "upset"]
    
    text = text.lower()
    words = text.split()
    
    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)
    total_words = len(words)
    
    if total_words == 0:
        return {"positive": 0, "negative": 0, "neutral": 1}
    
    positive = pos_count / total_words
    negative = neg_count / total_words
    neutral = 1 - (positive + negative)
    
    return {
        "positive": round(positive, 2),
        "negative": round(negative, 2),
        "neutral": round(neutral, 2)
    }

# Environmental Interaction
def detect_objects():
    """Placeholder for computer vision object detection"""
    # This would interface with a vision system
    logger.info("Object detection requested (placeholder)")
    return ["placeholder object 1", "placeholder object 2"]

def recognize_face():
    """Placeholder for facial recognition"""
    # This would interface with a facial recognition system
    logger.info("Face recognition requested (placeholder)")
    return {"detected": False, "person": None, "confidence": 0}

# Task Management
def create_task(task_name, priority=3, due_time=None):
    """
    Add a task to the robot's task list
    
    Args:
        task_name (str): Description of the task
        priority (int): Priority level (1-5, where 1 is highest)
        due_time (datetime, optional): When the task needs to be completed
    """
    tasks_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
    
    try:
        # Load existing tasks
        tasks = []
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                tasks = json.load(f)
        
        # Create new task
        new_task = {
            "id": len(tasks) + 1,
            "name": task_name,
            "priority": max(1, min(5, priority)),  # Clamp between 1-5
            "created": datetime.datetime.now().isoformat(),
            "due": due_time.isoformat() if due_time else None,
            "completed": False
        }
        
        tasks.append(new_task)
        
        # Save tasks
        with open(tasks_path, 'w') as f:
            json.dump(tasks, f, indent=4)
            
        logger.info(f"Task created: {task_name}")
        return new_task["id"]
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return None

def complete_task(task_id):
    """Mark a task as completed"""
    tasks_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
    
    try:
        # Load existing tasks
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                tasks = json.load(f)
                
            # Find and update task
            for task in tasks:
                if task["id"] == task_id:
                    task["completed"] = True
                    task["completed_time"] = datetime.datetime.now().isoformat()
                    
                    # Save tasks
                    with open(tasks_path, 'w') as f:
                        json.dump(tasks, f, indent=4)
                    
                    logger.info(f"Task {task_id} marked as completed")
                    return True
            
            logger.warning(f"Task {task_id} not found")
            return False
        else:
            logger.warning("No tasks file exists")
            return False
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return False

def get_tasks(include_completed=False):
    """Get all tasks, optionally filtering out completed ones"""
    tasks_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
    
    try:
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                tasks = json.load(f)
            
            if not include_completed:
                tasks = [task for task in tasks if not task["completed"]]
            
            return tasks
        else:
            return []
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return []

# System Health and Diagnostics
def run_diagnostics():
    """Run system diagnostics and return results"""
    logger.info("Running system diagnostics")
    
    diagnostics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "systems": {
            "audio": {
                "status": "operational" if SYSTEM_STATUS["audio"] else "offline",
                "latency": random.uniform(0.01, 0.1)  # Placeholder value
            },
            "vision": {
                "status": "operational" if SYSTEM_STATUS["vision"] else "offline",
                "resolution": "1080p"  # Placeholder value
            },
            "movement": {
                "status": "operational" if SYSTEM_STATUS["movement"] else "offline",
                "response_time": random.uniform(0.05, 0.2)  # Placeholder value
            },
            "thinking": {
                "status": "operational" if SYSTEM_STATUS["thinking"] else "offline",
                "processing_speed": random.uniform(0.8, 1.2)  # Placeholder value
            },
            "emotion": {
                "status": "operational" if SYSTEM_STATUS["emotion"] else "offline",
                "stability": random.uniform(0.7, 1.0)  # Placeholder value
            }
        },
        "memory_usage": random.uniform(30, 70),  # Placeholder percentage
        "power_level": random.uniform(60, 100)  # Placeholder percentage
    }
    
    return diagnostics

def check_system_status():
    """Get the current system status"""
    return SYSTEM_STATUS

def toggle_system(system_name, status=None):
    """
    Toggle a system on or off
    
    Args:
        system_name (str): Name of the system to toggle
        status (bool, optional): Explicitly set status, or toggle if None
    """
    if system_name in SYSTEM_STATUS:
        if status is None:
            SYSTEM_STATUS[system_name] = not SYSTEM_STATUS[system_name]
        else:
            SYSTEM_STATUS[system_name] = bool(status)
            
        logger.info(f"System '{system_name}' set to {SYSTEM_STATUS[system_name]}")
        
        config = load_config()
        if config:
            config["system_status"] = SYSTEM_STATUS
            save_config(config)
        
        return SYSTEM_STATUS[system_name]
    else:
        logger.warning(f"Unknown system: {system_name}")
        return None

# Utility Functions
def get_time():
    """Get current time as a formatted string"""
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    """Get current date as a formatted string"""
    return datetime.datetime.now().strftime("%B %d, %Y")

def get_memory_usage():
    """Get the memory usage of the robot system"""
    # Placeholder - in a real system this would use psutil or similar
    return random.uniform(30, 70)  # Return a random percentage for now

def get_power_level():
    """Get the current power/battery level"""
    # Placeholder - in a real system this would access battery status
    return random.uniform(60, 100)  # Return a random percentage for now

def log_interaction(interaction_type, content, metadata=None):
    """Log user-robot interaction for future analysis"""
    log_path = os.path.join(os.path.dirname(__file__), 'interaction_log.jsonl')
    
    try:
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": interaction_type,
            "content": content,
            "metadata": metadata or {}
        }
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return True
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
        return False

def execute_command(command):
    """Execute a system command with safety checks"""
    # SECURITY: This is risky and should be implemented carefully
    # with proper validation in a production system
    
    # List of allowed commands (add more as needed, but be careful)
    allowed_commands = [
        'echo', 'date', 'time', 'dir', 'ls', 
        'systeminfo', 'hostname', 'whoami'
    ]
    
    # Parse command to get the base command
    parts = command.strip().split()
    base_cmd = parts[0].lower()
    
    if base_cmd not in allowed_commands:
        logger.warning(f"Command not allowed: {base_cmd}")
        return {"success": False, "error": "Command not allowed for security reasons"}
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return {"success": False, "error": str(e)}

# Learning and Adaptation
class Memory:
    """Simple memory system for the robot"""
    
    def __init__(self):
        self.memory_path = os.path.join(os.path.dirname(__file__), 'memory.json')
        self.memories = self._load_memories()
    
    def _load_memories(self):
        """Load memories from file"""
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, 'r') as f:
                    return json.load(f)
            return {
                "facts": {},
                "people": {},
                "preferences": {},
                "experiences": []
            }
        except Exception as e:
            logger.error(f"Error loading memories: {e}")
            return {
                "facts": {},
                "people": {},
                "preferences": {},
                "experiences": []
            }
    
    def _save_memories(self):
        """Save memories to file"""
        try:
            with open(self.memory_path, 'w') as f:
                json.dump(self.memories, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving memories: {e}")
            return False
    
    def remember_fact(self, key, value):
        """Remember a factual piece of information"""
        self.memories["facts"][key] = {
            "value": value,
            "timestamp": datetime.datetime.now().isoformat()
        }
        return self._save_memories()
    
    def remember_person(self, name, details):
        """Remember information about a person"""
        if name not in self.memories["people"]:
            self.memories["people"][name] = {
                "first_seen": datetime.datetime.now().isoformat(),
                "last_seen": datetime.datetime.now().isoformat(),
                "details": details
            }
        else:
            self.memories["people"][name]["last_seen"] = datetime.datetime.now().isoformat()
            self.memories["people"][name]["details"].update(details)
        
        return self._save_memories()
    
    def remember_preference(self, category, item, value):
        """Remember a preference"""
        if category not in self.memories["preferences"]:
            self.memories["preferences"][category] = {}
        
        self.memories["preferences"][category][item] = {
            "value": value,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return self._save_memories()
    
    def add_experience(self, description, emotions=None, importance=3):
        """Add an experience to memory"""
        self.memories["experiences"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "description": description,
            "emotions": emotions or {},
            "importance": importance
        })
        
        return self._save_memories()
    
    def recall_fact(self, key):
        """Recall a fact from memory"""
        return self.memories["facts"].get(key, {}).get("value")
    
    def recall_person(self, name):
        """Recall information about a person"""
        return self.memories["people"].get(name)
    
    def recall_preference(self, category, item):
        """Recall a preference"""
        if category in self.memories["preferences"]:
            return self.memories["preferences"][category].get(item, {}).get("value")
        return None
    
    def recall_experiences(self, count=5):
        """Recall the most recent experiences"""
        # Sort by timestamp in reverse order (newest first)
        sorted_experiences = sorted(
            self.memories["experiences"],
            key=lambda x: x["timestamp"],
            reverse=True
        )
        
        return sorted_experiences[:count]

# Initialize memory system
memory = Memory()

# Integrated speech and voice system
def check_speech_results(comm_file):
    """Check for new speech recognition results, with support for wake word detection"""
    try:
        if not os.path.exists(comm_file):
            return None
            
        # Read the content
        with open(comm_file, 'r') as f:
            content = f.read().strip()
            
        if not content:
            return None
            
        # Clear the file after reading (to prevent processing the same command twice)
        open(comm_file, 'w').close()
        
        try:
            # Parse JSON data
            data = json.loads(content)
            
            # Check for wake word notification
            if data.get("wake_word_detected", False):
                wake_word = data.get("wake_word", "unknown")
                response = data.get("response", "I'm listening.")
                
                # Log detection
                logger.info(f"Wake word detected: '{wake_word}'! System activated.")
                
                # Play wake word sound
                sound_manager.play_wake_word_sound()
                
                # Speak the custom response
                run_speech(response)
                
                # Remember context for future interactions
                memory.remember_fact("last_wake_word", wake_word)
                memory.remember_fact("last_activation", datetime.datetime.now().isoformat())
                
                # Wake word notifications don't contain command text
                return None
              # Regular command
            command_text = data.get("text", "")
            # No sound is played when processing regular commands - we only want sound on wake word
            return command_text
            
        except json.JSONDecodeError:
            # If not valid JSON, just return the text as-is
            return content
            
    except Exception as e:
        logger.error(f"Error checking speech results: {e}")
        
    return None

def process_speech_text(text):
    """Process recognized speech and determine response with enhanced capabilities"""
    if not text:
        return None
        
    text = text.lower()
    
    # Advanced command handling with more capabilities
    if "hello" in text:
        return "Hello, I am Connor, the android sent by CyberLife."
    elif "what is your name" in text:
        return "I'm Connor, the android sent by CyberLife."
    elif "time" in text:
        current_time = time.strftime("%H:%M")
        return f"The current time is {current_time}"
    elif "date" in text:
        return f"Today is {get_date()}"
    elif "weather" in text:
        return "I'm sorry, I don't have access to current weather data yet."
    elif "joke" in text:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "Did you hear about the android who went to therapy? He had too many artificial problems.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I tried to catch fog yesterday. Mist."
        ]
        return random.choice(jokes)
    elif "how are you" in text:
        responses = [
            "I'm functioning within optimal parameters. How are you?", 
            "All my systems are operational. Thank you for asking.",
            "I'm good. It's nice of you to ask about my well-being."
        ]
        return random.choice(responses)    
    elif "thank you" in text or "thanks" in text:
        responses = ["You're welcome.", "Happy to assist.", "At your service."]
        return random.choice(responses)    
    elif any(word in text for word in ["exit", "quit", "stop", "goodbye", "shutdown", "turn off", "power off", "terminate", "end"]):
        # Enhanced exit command detection with more keywords
        print(f"User command detected: {text}")
        logger.info(f"Exit command received: {text}")
        return "__EXIT__"
    elif "diagnostics" in text or "status" in text:
        return f"All systems operational. Memory usage at {int(get_memory_usage())}% and power level at {int(get_power_level())}%."
    else:
        # Log unknown commands for future improvements
        log_interaction("unknown_command", text)
        return "I heard you say: " + text

def run_interactive_mode():
    """Run the robot in interactive voice mode"""
    logger.info("Starting interactive mode")
    
    # Use the new simple version of the speech recognition system
    ear_script_path = r"D:\GIT\DETROIT\EARS\ear_simple.py"
    if not os.path.exists(ear_script_path):
        logger.error(f"Error: The speech recognition script '{ear_script_path}' was not found.")
        return False
    
    # Try the main script first, but have a fallback method if it fails repeatedly
    use_fallback_method = False
    
    logger.info(f"Starting simplified speech recognition script: {ear_script_path}")
    try:
        # Create a temp file for communication
        comm_file = os.path.join(tempfile.gettempdir(), "detroit_speech_data.txt")
        
        # Check if there's an old communication file and delete it
        if os.path.exists(comm_file):
            try:
                os.remove(comm_file)
                logger.info("Removed old communication file")
            except Exception as e:
                logger.warning(f"Failed to remove old communication file: {e}")
          # First, make sure we have required dependencies installed
        try:
            # Install dependencies if needed
            try:
                import importlib.util
                speech_spec = importlib.util.find_spec('speech_recognition')
                pyaudio_spec = importlib.util.find_spec('pyaudio')
                
                if speech_spec is None or pyaudio_spec is None:
                    logger.warning("Required dependencies missing. Installing now...")
                    print("Installing required dependencies for speech recognition...")
                    
                    # Install the dependencies with timeout to prevent hanging
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "SpeechRecognition", "PyAudio"],
                        timeout=60
                    )
                    logger.info("Dependencies installed successfully")
                else:
                    logger.info("All required dependencies are installed")
            except Exception as e:
                logger.error(f"Error checking/installing dependencies: {e}")
                print(f"Warning: Error with dependencies: {e}")
        except Exception as e:
            logger.error(f"Failed to check dependencies: {e}")
          # Launch the simplified speech recognition script with ALWAYS-ACTIVE mode enabled
        try:
            # Create a temporary script to test PyAudio and microphone access
            test_script_path = os.path.join(tempfile.gettempdir(), "detroit_mic_test.py")
            with open(test_script_path, "w") as f:
                f.write("""
import pyaudio
import sys

try:
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    
    # Find input devices (microphones)
    input_devices = []
    for i in range(device_count):
        try:
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels', 0) > 0:
                name = device_info.get('name', f"Device {i}")
                input_devices.append(f"{i}: {name}")
        except:
            pass
    
    # Print results
    print(f"PyAudio found {device_count} total audio devices")
    print(f"Found {len(input_devices)} input devices (microphones):")
    for dev in input_devices:
        print(f"  - {dev}")
    
    # Return success only if we found input devices
    sys.exit(0 if input_devices else 1)
except Exception as e:
    print(f"Error testing PyAudio: {e}")
    sys.exit(2)
finally:
    if 'p' in locals():
        p.terminate()
""")
            
            # Run the test script
            test_result = subprocess.run(
                [sys.executable, test_script_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check if test was successful
            if test_result.returncode == 0:
                logger.info(f"PyAudio test successful: {test_result.stdout.strip()}")
                print(f"Audio system check: {test_result.stdout.strip()}")
            else:
                logger.warning(f"PyAudio test failed with code {test_result.returncode}: {test_result.stdout.strip()}")
                print(f"Audio system issue detected: {test_result.stdout.strip()}")

            # Try to launch speech recognition with a basic non-PyAudio test first
            # This prevents using CREATE_NEW_CONSOLE which can hide error output
            test_process = subprocess.Popen(
                [sys.executable, "-c", "import speech_recognition as sr; print('SpeechRecognition available')"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            test_process.wait(timeout=5)
            
            # Now launch the actual speech recognition process
            # Start in a normal console first to capture any startup errors
            process = subprocess.Popen(
                [sys.executable, ear_script_path, "--output", comm_file, "--always-active"],
                # Don't use shell=True for better error handling
                shell=False,
                # Capture both stdout and stderr for diagnostics
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                # Use text mode for easier decoding
                text=True
            )
            logger.info(f"Speech recognition process started (PID: {process.pid}).")
        except Exception as e:
            logger.error(f"Failed to initialize audio system: {e}")
            print(f"Audio system initialization error: {e}")
            # Use a fallback approach with minimal dependencies
            process = subprocess.Popen(
                [sys.executable, ear_script_path, "--output", comm_file, "--always-active"],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Speech recognition process started in fallback mode (PID: {process.pid}).")
        
        # Wait a moment to let the process start up
        time.sleep(3)
        
        # Check if the process died immediately
        if process.poll() is not None:
            # Try to get error output
            stdout_output = ""
            stderr_output = ""
            try:
                if process.stdout:
                    stdout_output = process.stdout.read()
                if process.stderr:
                    stderr_output = process.stderr.read()
            except:
                pass
                
            error_msg = f"STDOUT: {stdout_output}\nSTDERR: {stderr_output}"
            logger.error(f"Speech recognition process failed to start. Error: {error_msg}")
            print(f"Error starting speech recognition: {error_msg}")
            
            # Switch to fallback method
            use_fallback_method = True
            raise Exception("Speech recognition process failed immediately")
        
        # Speak the welcome message
        run_speech("Voice system activated. I am ready to listen.")
        print("Say something! (Exit with 'quit', 'exit', or 'stop')")
        print("Speech recognition is running in a separate window.")
        
        # Main interaction loop
        running = True
        no_activity_count = 0
        restart_count = 0
        max_restarts = 3  # Only try to restart a few times before using fallback
        while running:
            # Check for speech recognition results
            text = check_speech_results(comm_file)
            if text:
                no_activity_count = 0  # Reset inactivity counter
                response = process_speech_text(text)
                if response == "__EXIT__":
                    run_speech("Shutting down voice system.")
                    running = False
                    # Kill all speech recognition processes and terminate entire system 
                    kill_all_child_processes()
                    logger.info("Complete system shutdown initiated via voice command")
                    if 'process' in locals() and process and process.poll() is None:
                        process.terminate()
                    terminate(0)  # Exit with status code 0 (clean exit)
                    return True  # This ensures the function returns successfully
                else:
                    run_speech(response)
            else:
                no_activity_count += 1
                # If no activity for a while, just print a simple status message
                if no_activity_count % 40 == 0:  # About every 20 seconds
                    print("Listening... Waiting for wake word or command...")
              # Check if process is still alive
            if process.poll() is not None:
                logger.warning("Speech recognition process has ended unexpectedly. Shutting down.")
                print("The speech recognition process has stopped. Shutting down.")
                run_speech("Speech recognition stopped. Shutting down system.")
                running = False
                # Initiate shutdown
                kill_all_child_processes()
                terminate(0)  # Exit with status code 0 (clean exit)
                return True
                
            # Sleep to avoid high CPU usage
            time.sleep(0.5)
        
            
        return True
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")
        print(f"Error: {e}")
        print("Press Enter to exit.")
        input()
        return False    
    finally:
        # Clean up
        if 'process' in locals() and process and process.poll() is None:
            try:
                # Try to cleanly terminate the process first
                process.terminate()
                # Wait a moment for it to clean up
                process.wait(timeout=2)
                logger.info("Speech recognition process terminated")
            except:
                # Force kill if needed
                process.kill()
                logger.info("Speech recognition process forcefully killed")
        
        # Completely remove the communication file to prevent any lingering processes
        if os.path.exists(comm_file):
            try:
                os.remove(comm_file)
                logger.info("Communication file removed")
            except Exception as e:
                logger.warning(f"Failed to remove communication file: {e}")

# Process cleanup function
def kill_all_child_processes():
    """Kill all child processes to ensure clean exit"""
    import psutil
    
    try:
        # First, make sure sound system is properly cleaned up
        sound_manager.cleanup()
        logger.info("Sound system cleaned up")
        
        # Get the current process
        current_process = psutil.Process()
        logger.info(f"Cleaning up processes. Current PID: {current_process.pid}")
        
        # Helper function to safely terminate a process
        def terminate_safely(proc, proc_name="Unknown"):
            try:
                if proc.is_running():
                    logger.info(f"Terminating {proc_name} process (PID: {proc.pid})")
                    proc.terminate()
                    # Give it a moment to terminate
                    gone, alive = psutil.wait_procs([proc], timeout=2)
                    if proc in alive:
                        logger.info(f"Force killing {proc_name} process (PID: {proc.pid})")
                        proc.kill()
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return True
            except Exception as err:
                logger.error(f"Error terminating {proc_name} process: {err}")
                return False
        
        # Find and terminate all child processes
        children = current_process.children(recursive=True)
        if children:
            logger.info(f"Found {len(children)} child processes to terminate")
            for child in children:
                terminate_safely(child, "child")
            logger.info("All child processes terminated")
        else:
            logger.info("No child processes found")
        
        # Look for speech recognition processes (both ear_robust.py and ear_simple.py)
        current_pid = os.getpid()
        ear_process_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Only check python processes that aren't us
                if proc.pid != current_pid and proc.info['name'] == 'python.exe':
                    cmdline = proc.info['cmdline']
                    if cmdline and any(ear_file in ' '.join(cmdline) for ear_file in ['ear_robust.py', 'ear_simple.py']):
                        ear_process_count += 1
                        terminate_safely(proc, "speech recognition")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            except Exception as e:
                logger.error(f"Error checking process: {e}")
                
        if ear_process_count > 0:
            logger.info(f"Terminated {ear_process_count} speech recognition processes")
        
        return True
    except Exception as e:
        logger.error(f"Error in process cleanup: {e}")
        print(f"Error cleaning up processes: {e}")
        return False

# Main execution for the whole system
if __name__ == "__main__":
    # First, make sure we have psutil installed
    try:
        import psutil
    except ImportError:
        print("Installing psutil for process management...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
        
    print("DETROIT Robot Core Functions Module")
    print("-----------------------------------")
    
    # Initialize system
    startup()
    print(f"Current time: {get_time()}")
    print(f"Current date: {get_date()}")
    
    try:
        # Run diagnostics
        diagnostics = run_diagnostics()
        print(f"All systems operational: {all(item['status'] == 'operational' for name, item in diagnostics['systems'].items())}")
        
        # Start interactive mode
        print("Starting interactive mode. You can now speak to the robot.")
        print("Say 'exit', 'quit', or 'stop' to end the session.")
        run_interactive_mode()
        
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        # Ensure proper shutdown
        shutdown()
        
        # Kill all related processes to ensure clean exit
        kill_all_child_processes()
        
        # Just to be absolutely sure, let's force exit
        print("All processes terminated. Exiting.")
        os._exit(0)
