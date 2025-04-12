"""
AI Command Parser for Smart Home Application

It uses a Hugging Face model to parse natural language commands
for controlling simulated smart home devices.
"""

from typing import Dict, Any, List, Optional

# Added for Hugging Face integration
from transformers import pipeline
import re

# Import shared constants
import config

class CommandParser:
    """
    Uses Hugging Face Transformers for zero-shot classification
    to parse natural language commands for smart home devices.
    """

    def __init__(self):
        """
        Initialize the command parser with devices, actions, and the classification pipeline.
        Raises RuntimeError if the Hugging Face model cannot be loaded.
        """
        # Use constants for device types
        self.supported_devices = config.SUPPORTED_DEVICES

        # Define action labels (could move to config if they become numerous)
        # Using f-strings with device constants for consistency
        self.device_actions = {
            config.DEVICE_LIGHT: [f"turn on {config.DEVICE_LIGHT}", f"turn off {config.DEVICE_LIGHT}", f"get {config.DEVICE_LIGHT} status"],
            config.DEVICE_FAN: [
                f"turn on {config.DEVICE_FAN}", f"turn off {config.DEVICE_FAN}",
                f"set {config.DEVICE_FAN} speed low", f"set {config.DEVICE_FAN} speed medium", f"set {config.DEVICE_FAN} speed high",
                f"get {config.DEVICE_FAN} status"
            ],
            config.DEVICE_THERMOSTAT: [
                f"set {config.DEVICE_THERMOSTAT} temperature", f"increase {config.DEVICE_THERMOSTAT} temperature",
                f"decrease {config.DEVICE_THERMOSTAT} temperature", f"get {config.DEVICE_THERMOSTAT} status"
            ]
        }
        self.all_possible_labels = [action for actions in self.device_actions.values() for action in actions]
        self.all_possible_labels.append("get status of all devices")
        self.classifier = None # Initialize classifier attribute

        # Load the zero-shot classification pipeline using model name from config
        try:
            print("Loading Hugging Face model...")
            self.classifier = pipeline("zero-shot-classification", model=config.MODEL_NAME)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Fatal Error: Could not load Hugging Face model: {e}")
            raise RuntimeError(f"Failed to load Hugging Face model: {e}")

    def parse_command(self, user_input: str) -> Dict[str, Any]:
        """
        Parse a natural language command using Hugging Face zero-shot classification.

        Args:
            user_input (str): The natural language command from the user

        Returns:
            dict: Structured command with device, action, and parameters, or an error dictionary.
        """
        if not self.classifier:
             # This case should ideally not be reached if __init__ raises an error
             return {"error": "Command parser model is not loaded."}

        try:
            # Perform classification
            classification = self.classifier(user_input, self.all_possible_labels, multi_label=False)

            # Get the highest probability label
            best_label = classification['labels'][0]
            best_score = classification['scores'][0]

            print(f"HF Classification: Label='{best_label}', Score={best_score:.4f}")

            # Confidence threshold from config
            CONFIDENCE_THRESHOLD = config.CLASSIFICATION_THRESHOLD
            if best_score < CONFIDENCE_THRESHOLD:
                 print(f"Confidence score {best_score:.4f} below threshold {CONFIDENCE_THRESHOLD}.")
                 return {"error": f"Could not confidently understand the command (Score: {best_score:.2f}). Please rephrase."}

            result = {
                "device": None,
                "action": None,
                "parameters": {},
                "is_query": False
            }

            # Map the best label back to device and action
            if best_label == "get status of all devices":
                result["device"] = "all"
                result["action"] = "status"
                result["is_query"] = True
            else:
                # Find which device this action belongs to
                for device, actions in self.device_actions.items():
                    if best_label in actions:
                        result["device"] = device
                        # Extract action type from the label
                        parts = best_label.split()
                        if parts[0] == "get":
                            result["action"] = "status"
                            result["is_query"] = True
                        elif parts[0] == "turn":
                            result["action"] = f"turn_{parts[1]}"
                        elif parts[0] == "set":
                            if "speed" in best_label:
                                result["action"] = "set_speed"
                                result["parameters"]["speed_level"] = parts[-1].upper()
                            elif "temperature" in best_label:
                                result["action"] = "set_temperature"
                                # Use regex to extract temperature from original input
                                temp_match = re.search(r'(\d+)(?:\s*°?C|\s*degrees)?', user_input)
                                if temp_match:
                                    result["parameters"]["temp"] = float(temp_match.group(1))
                                else:
                                     # If keyword matched but value didn't, ask for value
                                     return {"error": f"Please specify the temperature value (e.g., 'set temperature to 22')."}
                        elif parts[0] in ["increase", "decrease"]:
                            result["action"] = f"{parts[0]}_temperature"
                            # Use regex to extract amount from original input if specified
                            # Use constant for default amount check if needed, though controller handles default
                            amount_match = re.search(r'by\s+(\d+)(?:\s*°?C|\s*degrees)?', user_input)
                            if amount_match:
                                result["parameters"]["amount"] = float(amount_match.group(1))
                        break # Stop searching once device/action is found

            # Error if mapping fails (shouldn't happen with current logic)
            if result["device"] is None or result["action"] is None:
                 print(f"Internal Error: Could not map label '{best_label}' to a device/action.")
                 return {"error": f"Internal error processing action: {best_label}"}

            return result

        except Exception as e:
            print(f"Error during Hugging Face parsing: {e}")
            return {"error": f"An error occurred during command parsing: {e}"}
