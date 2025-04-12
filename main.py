"""
Smart Home Application CLI

This module provides a command-line interface for interacting with the smart home system.
"""

import sys
import time
from controller import SmartHomeController

# Import shared constants
import config

def display_welcome():
    """Display welcome message and instructions."""
    print("\n" + "="*60)
    print("       SMART HOME ASSISTANT WITH AI COMMAND PROCESSING       ")
    print("="*60)
    print("\nAvailable devices:")
    print("  - Light (can be turned ON/OFF)")
    print("  - Fan (can be turned ON/OFF and set to LOW, MEDIUM, or HIGH speed)")
    print("  - Thermostat (can be set between 18°C and 30°C)")
    print("\nExample commands:")
    print("  - 'Turn on the light'")
    print("  - 'Set the fan speed to high'")
    print("  - 'What is the current temperature?'")
    print("  - 'What is the status of all devices?'")
    print("  - 'Exit' or 'Quit' to end the program")
    print("\n" + "-"*60)

def main():
    """Main function to run the smart home application."""
    # Initialize the controller
    controller = SmartHomeController()
    
    # Display welcome message
    display_welcome()
    
    # Main interaction loop
    while True:
        # Get user input
        user_input = input("\n> Enter a command: ").strip()
        
        # Check for exit command using constants from config
        if user_input.lower() in config.EXIT_COMMANDS:
            print("\nThank you for using the Smart Home Assistant. Goodbye!")
            break
        
        # Skip empty input
        if not user_input:
            continue
        
        # Process the command
        print("\nProcessing command...")
        # Add a small delay to simulate processing time
        # time.sleep(0.5) # Removed artificial delay
        
        # Get the response
        response = controller.process_command(user_input)
        
        # Display the response
        print(f"\nResponse: {response}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)
