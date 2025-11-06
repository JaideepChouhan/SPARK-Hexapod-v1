# filepath: d:\GIT\DETROIT\BRAIN\direct_runner.py
"""
Direct runner script that imports and runs all necessary components together
to avoid module import issues.
"""

import os
import sys
import subprocess
import tempfile
import time
import json
import logging
import importlib.util  # Add this import for dynamic module loading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'detroit_log.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DETROIT.RUNNER')

def ensure_path(path):
    """Ensure a path is in sys.path"""
    if path not in sys.path:
        sys.path.insert(0, path)

# Add all project paths to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
brain_path = os.path.join(project_root, 'BRAIN')
ears_path = os.path.join(project_root, 'EARS')
vocal_cords_path = os.path.join(project_root, 'VOCAL_CORDS')

ensure_path(brain_path)
ensure_path(ears_path)
ensure_path(vocal_cords_path)

# Print paths for debugging
print(f"Project root: {project_root}")
print(f"Python path includes: {brain_path}, {ears_path}, {vocal_cords_path}")

# Directly import functions module
import functions

def load_module_from_file(file_path, module_name):
    """Load a module directly from a file path"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Error loading module {module_name} from {file_path}: {e}")
        return None

def setup_voice_system():
    """Set up the voice system directly"""
    # We need to manually load the voice module
    voice_path = os.path.join(vocal_cords_path, 'voice.py')
    ear_path = os.path.join(ears_path, 'ear.py')
    
    try:
        # Load modules directly from file paths
        voice_module = load_module_from_file(voice_path, "voice_module")
        ear_module = load_module_from_file(ear_path, "ear_module")
        
        if not voice_module:
            logger.error("Failed to load voice module")
            return False
            
        logger.info("Starting speech recognition process")
        result = voice_module.run_speech_recognition()
        
        if result and len(result) == 2:
            stt_process, comm_file = result
            logger.info(f"Speech recognition started (PID: {stt_process.pid})")
            
            # Run the voice interaction loop
            voice_module.speak("System initialization complete. Voice system activated.")
            print("Say something! (Exit with 'quit', 'exit', or 'stop')")
            
            voice_module.run_voice_interaction_loop(stt_process, comm_file)
            return True
        else:
            logger.error("Failed to start speech recognition")
            return False
    except Exception as e:
        logger.error(f"Error setting up voice system: {e}")
        return False

def run():
    """Run the Detroit system with direct imports"""
    print("DETROIT Robot Core Functions Module - Direct Runner")
    print("--------------------------------------------------")
    
    # Initialize system
    functions.startup()
    print(f"Current time: {functions.get_time()}")
    print(f"Current date: {functions.get_date()}")
    
    try:
        # Run diagnostics
        diagnostics = functions.run_diagnostics()
        print(f"All systems operational: {all(item['status'] == 'operational' for name, item in diagnostics['systems'].items())}")
        
        # Start voice system directly (bypassing module import issues)
        print("Starting interactive mode. You can now speak to the robot.")
        print("Say 'exit', 'quit', or 'stop' to end the session.")
        
        setup_voice_system()
        
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        # Ensure proper shutdown
        functions.shutdown()

if __name__ == "__main__":
    run()
