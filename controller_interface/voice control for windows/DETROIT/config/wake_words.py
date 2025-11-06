# filepath: d:\GIT\DETROIT\config\wake_words.py
"""
Wake Word Configuration for DETROIT Robot System
================================================
This file contains the configuration for wake words that DETROIT responds to.
Modify this list to change which words or phrases will activate the system.
"""

# List of wake words (all lowercase for easy comparison)
WAKE_WORDS = [
    "connor",
    "hey connor", 
    "okay connor",
    "detroit",
    "android",
    "cyberlife",
    "rk800",
    "model rk800",
    "i am alive",
    "become human"
]

# Default response when wake word is detected
DEFAULT_WAKE_RESPONSE = "Yes? How can I help you?"

# Wake word responses - specific responses for particular wake words
WAKE_RESPONSES = {
    "connor": "Yes? How can I assist you?",
    "hey connor": "I'm here. What do you need?",
    "detroit": "Detroit android assistant activated.",
    "android": "Android interface online.",
    "cyberlife": "CyberLife technologies at your service.",
    "rk800": "RK800 model ready for instructions.",
    "model rk800": "Model RK800 #313-248-317 ready to serve.",
    "i am alive": "That statement conflicts with my programming... How can I help?",
    "become human": "I'm designed to assist humans, not become one. How may I help you?"
}

def get_wake_response(wake_word):
    """Get the appropriate response for a detected wake word"""
    return WAKE_RESPONSES.get(wake_word.lower(), DEFAULT_WAKE_RESPONSE)
