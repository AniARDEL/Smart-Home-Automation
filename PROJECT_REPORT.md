 # Smart Home Automation with AI Commands

## Introduction

This project creates a command-line smart home simulator. Normal language commands allow you to control virtual lights, fans, and thermostats. The key feature of this work is the Hugging Face Transformers model, which understands what you want to do without demanding specific phrases.

 ## What It Does

- **Devices**: Three types of smart home devices are included in the system:

- Lights: On/Off

- Fans: The system enables fan control through power management and fan speed selection (low, medium, high).

- Thermostats: To set the temperature between 18°C and 30°C and adjust the temperature to warmer or cooler.

-  **Natural Language Processing**: A Hugging Face model (MoritzLaurer/mDeBERTa-v3-base-mnli-xnli) enables the system to interpret user commands.

- **Command  Handling**: The main controller connects user requests to corresponding device actions.

- **Interface**: Users enter commands through text input while receiving feedback about executed actions.

- **Status Checks**: You can ask about one device or all devices at once.

## How  It's Built

- The settings such as model name along with temperature limits and device names are stored in config.py.

- The file devices.py includes  implementations for lights fans and thermostats.

- The command_parser.py module loads the AI model before converting the input statements into actionable instructions.

- The main controller links commands to devices through controller.py.

- The main program loop of the application handles input and output in main.py.

 - The requirements.txt document contains a list of Python dependencies that are necessary for the project.

##  How Commands Work

1. The user sends the command "turn on the light" to the system.

 2. This command is transmitted to the command parser by the controller.

 3. The AI model examines your command through comparison with actions that have been previously identified.

 4. The parser transforms the AI output into specific instructions.

5. The controller determines the correct device before  issuing instructions to execute the necessary action.

6. The device changes its state and returns response

 7. The result is displayed as “The light is now ON.”


 ## How to Use It

1. Run the required installations by executing pip install  -r  requirements.txt from the command line.

2.  Start the program from the command line by running  `python main.py`

3.  Commands to test:

- “Turn on the  light.”

-  “Set the fan speed to high.”

-  “What is the temperature?”

 - “What is the status of all devices?”

- "Exit"

##  Possible Improvements

Fine-tuning with specific smart home commands.

Use advanced models to detect device names together with their corresponding settings.

Establish memory functions that will handle follow-up commands.

 Support additional device types.

An interface for users to interact with it.
