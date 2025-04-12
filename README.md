# Smart Home Application with AI Command Processing

This project implements a simple smart home application that allows users to control and monitor various devices (lights, fans, and thermostats) using natural language commands processed by a Hugging Face Transformers model.

## Project Structure

- `config.py`: Holds configuration constants (model name, thresholds, default names, etc.).
- `devices.py`: Contains classes for simulating smart home devices (Light, Fan, Thermostat)
- `command_parser.py`: Implements command parsing using a Hugging Face zero-shot classification model (configured via `config.py`).
- `controller.py`: Connects the command parser with device classes and handles command execution (uses settings from `config.py`).
- `main.py`: Provides a command-line interface for user interaction (uses settings from `config.py`).
- `requirements.txt`: Lists Python dependencies (`transformers`, `torch`, `tf-keras`).
- `PROJECT_REPORT.md`: Detailed documentation of the project (formerly `project_report.md`).

## Features

- Control lights (turn ON/OFF)
- Control fans (turn ON/OFF, set speed to LOW/MEDIUM/HIGH)
- Control thermostats (set temperature, increase/decrease temperature)
- Query device status (individual or all devices)
- Natural language command processing via Hugging Face Transformers

## Sample Commands and Expected Outputs

Here are some examples of commands you can try and the typical responses you might see:

1.  **Command:** `Turn on the living room light`
    **Output:** `Response: The Living Room Light is now ON.`

2.  **Command:** `Set the fan speed to medium`
    **Output:** `Response: The Living Room Fan speed is set to MEDIUM.`

3.  **Command:** `Set the temperature to 25 degrees`
    **Output:** `Response: The Living Room Thermostat is set to 25.0°C.`

4.  **Command:** `What's the fan status?`
    **Output:** `Response: Living Room Fan: ON (Speed: MEDIUM)` _(Assuming it was set previously)_

5.  **Command:** `What is the status of all devices?`
    **Output:**
    ```
    Response: Current Status:
    Living Room Light: ON
    Living Room Fan: ON (Speed: MEDIUM)
    Living Room Thermostat: 25.0°C
    ```
    _(Note: Actual status will depend on previous commands)_

## How to Run

1.  Make sure you have Python 3.6+ installed.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    _(Note: The first time you run the application, the Hugging Face model will be downloaded, which might take some time depending on your internet connection.)_
3.  Navigate to the project directory.
4.  Run the application:
    ```bash
    python main.py
    ```
5.  Enter commands at the prompt (e.g., `Turn off the fan`, `exit`).

## Testing

(Test file `test.py` was removed as part of cleanup.)

## Configuration

Key settings like the Hugging Face model name, classification confidence threshold, and default device names can be adjusted in the `config.py` file.

## Future Enhancements

- More sophisticated NLP models or fine-tuning for better accuracy.
- Handling more complex commands or conversation context.
- Integration with real AI models (OpenAI API)
- Additional device types
- Multi-room support
- User authentication
- Graphical user interface
- Voice input capabilities
- Scheduling and automation features
