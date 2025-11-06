# filepath: d:\GIT\DETROIT\config\settings.py
"""
Central Configuration for DETROIT Robot System
==============================================
This file contains all the configurable settings for the DETROIT robot system.
"""

# Wake Word Settings
WAKE_WORDS = [
    "connor",
    "hey connor", 
    "okay connor",
    "detroit",
    "android",
    "cyberlife",
    "rk800",
    "model rk800"
]

# Wake Word Response Settings - Customize what Detroit says when each wake word is detected
WAKE_RESPONSES = {
    "connor": "Yes? How can I assist you?",
    "hey connor": "I'm here. What do you need?",
    "okay connor": "Ready for your instructions.",
    "detroit": "Detroit android assistant activated.",
    "android": "Android interface online.",
    "cyberlife": "CyberLife technologies at your service.",
    "rk800": "RK800 model ready for instructions.",
    "model rk800": "Model RK800 #313-248-317 ready to serve."
}

# Sound Settings
SOUND_FILES = {
    "startup": "bankai.mp3",
    "shutdown": "no_like_rain.mp3",
    "wake_word": "nakime_biwa_sound.mp3",
    "command": "nakime_biwa_sound.mp3"  # Set to None to disable command sounds
}

# Speech Settings
SPEECH_SETTINGS = {
    "rate": 150,
    "volume": 1.0
}

def get_wake_response(wake_word):
    """Get the appropriate response for the detected wake word"""
    if not wake_word:
        return "How can I help you?"
    
    # Try to find an exact match first
    if wake_word.lower() in WAKE_RESPONSES:
        return WAKE_RESPONSES[wake_word.lower()]
    
    # Otherwise, try to find any partial match
    for word, response in WAKE_RESPONSES.items():
        if word in wake_word.lower():
            return response
    
    # Default response if no match is found
    return "How can I help you?"
