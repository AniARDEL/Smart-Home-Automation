# Project Report: Smart Home Automation with AI Commands

## 1. Introduction

This project implements a command-line smart home simulation system. Users can interact with simulated devices (lights, fans, thermostats) using natural language commands. The core innovation lies in using a pre-trained Hugging Face Transformers model to interpret these commands, offering a more flexible and intuitive user experience compared to rigid, predefined command structures.

## 2. Functionality

- **Device Simulation:** The system simulates three common smart home devices:
  - `Light`: Can be turned ON or OFF.
  - `Fan`: Can be turned ON or OFF, with speeds set to LOW, MEDIUM, or HIGH.
  - `Thermostat`: Temperature can be set within a range (18°C - 30°C), increased, or decreased.
- **Natural Language Processing (NLP):** User commands are processed using a zero-shot classification pipeline from the Hugging Face `transformers` library (specifically, the `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` model). This model classifies the user's intent based on predefined labels corresponding to device actions (e.g., "turn on light", "set fan speed medium", "get thermostat status").
- **Command Execution:** The main controller maps the classified intent to the corresponding method call on the target simulated device.
- **User Interface:** A simple Command-Line Interface (CLI) allows users to type commands and receive textual feedback about the action taken or the status of devices.
- **Status Queries:** Users can query the status of individual devices or all devices simultaneously.

## 3. Implementation Details

- **`config.py`:** A central configuration file holding constants such as the Hugging Face model name, classification threshold, default device names, temperature limits, and device type keys. This promotes maintainability and ease of modification.
- **`devices.py`:** Contains the Python classes (`Light`, `Fan`, `Thermostat`) defining the state and methods for each simulated device. Uses constants from `config.py` for default names and settings (like temperature limits).
- **`command_parser.py`:** Initializes the Hugging Face pipeline (using model name from `config.py`) and contains the `parse_command` method. This method takes raw user input, uses the zero-shot classifier (with threshold from `config.py`) to determine the best matching action label, and translates this label into a structured dictionary. Uses device type constants from `config.py`.
- **`controller.py`:** The `SmartHomeController` class acts as the central coordinator. It initializes device instances using default names and keys from `config.py`, and holds the command parser instance. Its `process_command` method gets the parsed command and calls `execute_command`, which uses device type constants from `config.py` to route actions and default values for parameters.
- **`main.py`:** Provides the main application loop, handles user input/output, displays welcome messages, and manages the program's lifecycle. Uses exit command constants from `config.py`.
- **`requirements.txt`:** Specifies the necessary Python libraries (`transformers`, `torch`, `tf-keras`).

## 4. Command Processing Flow

The process for handling a user command involves the interaction of several components:

1.  **Input (`main.py`):** The user enters a natural language command into the command-line interface managed by `main.py`.
2.  **Delegation (`main.py` -> `controller.py`):** `main.py` passes the raw command string to the `process_command` method of the `SmartHomeController` instance in `controller.py`.
3.  **Parsing (`controller.py` -> `command_parser.py`):** The controller calls the `parse_command` method in `command_parser.py`.
4.  **AI Classification (`command_parser.py` -> Hugging Face):** The `CommandParser` uses the loaded Hugging Face zero-shot classification pipeline to analyze the command against predefined action labels (e.g., "turn on light", "set fan speed medium").
5.  **Interpretation (`command_parser.py`):** The parser receives the highest-scoring label from the model, checks its confidence (using threshold from `config.py`), and maps it to a structured dictionary containing the target `device`, `action`, and extracted `parameters`. If confidence is low or parameters are missing (when required), an error dictionary is generated.
6.  **Execution (`controller.py` -> `devices.py`):** The controller receives the parsed dictionary. If it's not an error, it identifies the target device object (e.g., an instance of the `Light` class from `devices.py`) and calls the corresponding method (e.g., `light_instance.turn_on()`), passing any necessary parameters. For a "status of all devices" command, it iterates through all devices calling `get_status`.
7.  **State Update & Feedback (`devices.py` -> `controller.py`):** The relevant method in the device class (in `devices.py`) updates the simulated device's state (e.g., sets `self.state = "ON"`) and returns a string describing the outcome (e.g., "The Living Room Light is now ON.").
8.  **Response (`controller.py` -> `main.py`):** The controller passes the feedback string (or any error message from parsing/execution) back to `main.py`.
9.  **Output (`main.py`):** `main.py` prints the final response to the user's console.

## 5. Usage

1. Install requirements: `pip install -r requirements.txt`
2. Run the application: `python main.py`
3. Enter commands like "turn on the light", "set fan high", "what is the temperature?", "status of all devices", or "exit".

## 6. Challenges and Limitations

- **Model Dependency:** The application requires downloading the Hugging Face model on the first run, which can take time and requires internet access initially.
- **NLP Accuracy:** Zero-shot classification is powerful but not perfect. Ambiguous commands or phrasing not anticipated in the labels might be misinterpreted or result in low confidence scores.
- **Parameter Extraction:** While the model identifies the _intent_ (e.g., set temperature), specific values (the actual temperature number) are still extracted using regular expressions from the original input. More advanced NLP techniques could integrate value extraction directly.
- **Context:** The system is stateless regarding conversation; each command is processed independently.
- **Error Handling:** Error handling is basic. More complex interactions or unexpected model behavior could lead to unhandled exceptions.

## 7. Potential Improvements

- **Fine-tuning:** For higher accuracy on specific smart home commands, fine-tuning a suitable NLP model could be beneficial.
- **More Sophisticated NLP:** Using models capable of named entity recognition (NER) to extract device names, locations (if added), and parameters more reliably.
- **State Management:** Incorporating dialogue management to handle follow-up commands or clarifications.
- **Broader Device Support:** Adding more simulated devices (e.g., smart plugs, cameras).
- **GUI/Web Interface:** Creating a graphical interface instead of a CLI.
