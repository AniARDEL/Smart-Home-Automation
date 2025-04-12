"""
Smart Home Controller

This module implements the main controller for the smart home application,
connecting the command parser with the device classes and handling command execution.
"""

from devices import Light, Fan, Thermostat
from command_parser import CommandParser

# Import shared constants
import config

class SmartHomeController:
    """
    Main controller for the smart home application.
    Manages devices and executes commands parsed from natural language input.
    """
    
    def __init__(self):
        """Initialize the controller with default devices using names from config."""
        # Initialize devices using constants for keys and default names
        self.devices = {
            config.DEVICE_LIGHT: Light(name=config.DEFAULT_LIGHT_NAME),
            config.DEVICE_FAN: Fan(name=config.DEFAULT_FAN_NAME),
            config.DEVICE_THERMOSTAT: Thermostat(name=config.DEFAULT_THERMOSTAT_NAME)
        }
        
        # Initialize command parser
        self.command_parser = CommandParser()
    
    def process_command(self, user_input):
        """
        Process a natural language command from the user.
        
        Args:
            user_input (str): The natural language command
            
        Returns:
            str: Response message to the user
        """
        # Parse the command
        parsed_command = self.command_parser.parse_command(user_input)
        
        # Check for parsing errors
        if "error" in parsed_command:
            return parsed_command["error"]
        
        # Execute the command
        return self.execute_command(parsed_command)
    
    def execute_command(self, parsed_command):
        """
        Execute a parsed command on the appropriate device.
        
        Args:
            parsed_command (dict): The parsed command structure
            
        Returns:
            str: Response message to the user
        """
        device_name = parsed_command["device"]
        action = parsed_command["action"]
        parameters = parsed_command["parameters"]
        
        # Handle "all devices" status query
        if device_name == "all" and action == "status":
            return self.get_all_devices_status()
        
        # Get the target device
        device = self.devices.get(device_name)
        if not device:
            return f"Device '{device_name}' not found."
        
        # Execute the appropriate action on the device
        try:
            # Use constants for device name comparison
            if device_name == config.DEVICE_LIGHT:
                if action == "turn_on":
                    return device.turn_on()
                elif action == "turn_off":
                    return device.turn_off()
                elif action == "status":
                    return device.get_status()
            
            elif device_name == config.DEVICE_FAN:
                if action == "turn_on":
                    return device.turn_on()
                elif action == "turn_off":
                    return device.turn_off()
                elif action == "set_speed":
                    speed_level = parameters.get("speed_level", "LOW")
                    return device.set_speed(speed_level)
                elif action == "status":
                    return device.get_status()
            
            elif device_name == config.DEVICE_THERMOSTAT:
                if action == "set_temperature":
                    # Use constant for default temperature
                    temp = parameters.get("temp", config.THERMOSTAT_DEFAULT_TEMP)
                    return device.set_temperature(temp)
                elif action == "increase_temperature":
                    # Use constant for default amount
                    amount = parameters.get("amount", config.THERMOSTAT_DEFAULT_ADJUST_AMOUNT)
                    return device.increase_temperature(amount)
                elif action == "decrease_temperature":
                    # Use constant for default amount
                    amount = parameters.get("amount", config.THERMOSTAT_DEFAULT_ADJUST_AMOUNT)
                    return device.decrease_temperature(amount)
                elif action == "status":
                    return device.get_status()
            
            # This case should be less likely if command parser maps correctly
            return f"Action '{action}' not supported for {device_name}."
        
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def get_all_devices_status(self):
        """
        Get the status of all devices.
        
        Returns:
            str: Status of all devices
        """
        status_lines = [device.get_status() for device in self.devices.values()]
        return "Current Status:\n" + "\n".join(status_lines)
