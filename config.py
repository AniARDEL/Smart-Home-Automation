# --- config.py ---

# NLP Model Configuration
MODEL_NAME = 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'
CLASSIFICATION_THRESHOLD = 0.6

# Device Types (used as keys)
DEVICE_LIGHT = "light"
DEVICE_FAN = "fan"
DEVICE_THERMOSTAT = "thermostat"
SUPPORTED_DEVICES = [DEVICE_LIGHT, DEVICE_FAN, DEVICE_THERMOSTAT]

# Default Device Names
DEFAULT_LIGHT_NAME = "Living Room Light"
DEFAULT_FAN_NAME = "Living Room Fan"
DEFAULT_THERMOSTAT_NAME = "Living Room Thermostat"

# Device Specific Settings
THERMOSTAT_MIN_TEMP = 18
THERMOSTAT_MAX_TEMP = 30
THERMOSTAT_DEFAULT_TEMP = 22
THERMOSTAT_DEFAULT_ADJUST_AMOUNT = 1

# Fan Speeds are defined within the Fan class in devices.py 
# FAN_SPEED_OFF = "OFF" ... etc.


# Exit commands for main loop
EXIT_COMMANDS = ['exit', 'quit', 'bye', 'goodbye'] 
