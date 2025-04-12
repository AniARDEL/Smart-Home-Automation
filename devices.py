"""
Smart Home Device Simulation Classes

This file contains classes to simulate various smart home devices:
- Light: Can be turned ON/OFF
- Fan: Can be turned ON/OFF and set to low, medium, or high speed
- Thermostat: Can adjust temperature between 18°C and 30°C
"""

# Import shared constants
import config

class Light:
    """Simulates a smart light that can be turned ON/OFF."""
    
    STATE_ON = "ON"
    STATE_OFF = "OFF"
    
    def __init__(self, name=config.DEFAULT_LIGHT_NAME):
        """Initialize a light with a default name and OFF state."""
        self.name = name
        self.state = self.STATE_OFF
    
    def turn_on(self):
        """Turn the light ON."""
        self.state = self.STATE_ON
        return f"The {self.name} is now {self.STATE_ON}."
    
    def turn_off(self):
        """Turn the light OFF."""
        self.state = self.STATE_OFF
        return f"The {self.name} is now {self.STATE_OFF}."
    
    def get_status(self):
        """Return the current status of the light."""
        return f"{self.name}: {self.state}"


class Fan:
    """Simulates a smart fan that can be turned ON/OFF and set to different speeds."""
    
    # Keep Fan speeds here as they are specific to the Fan's internal logic
    SPEED_OFF = "OFF"
    SPEED_LOW = "LOW"
    SPEED_MEDIUM = "MEDIUM"
    SPEED_HIGH = "HIGH"
    
    SPEEDS = [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]
    
    STATE_ON = "ON"
    STATE_OFF = "OFF"
    
    # Speed index mapping
    SPEED_INDEX_OFF = 0
    SPEED_INDEX_LOW = 1
    SPEED_INDEX_MEDIUM = 2
    SPEED_INDEX_HIGH = 3
    
    def __init__(self, name=config.DEFAULT_FAN_NAME):
        """Initialize a fan with a default name, OFF state, and speed level 0."""
        self.name = name
        self.state = self.STATE_OFF
        self.speed = self.SPEED_INDEX_OFF
    
    def turn_on(self):
        """Turn the fan ON at the lowest speed."""
        if self.state == self.STATE_OFF:
            self.state = self.STATE_ON
            self.speed = self.SPEED_INDEX_LOW
        # Return status reflecting the change
        speed_str = self.SPEEDS[self.speed]
        return f"The {self.name} is now {self.state} at {speed_str} speed."
    
    def turn_off(self):
        """Turn the fan OFF."""
        self.state = self.STATE_OFF
        self.speed = self.SPEED_INDEX_OFF
        return f"The {self.name} is now {self.state}."
    
    def set_speed(self, speed_level):
        """
        Set the fan speed.
        
        Args:
            speed_level (str): The desired speed level ("LOW", "MEDIUM", "HIGH")
        
        Returns:
            str: Confirmation message
        """
        speed_level = speed_level.upper()
        if speed_level not in self.SPEEDS[1:]:  # Exclude "OFF" from valid inputs
            return f"Invalid speed level. Choose from: {', '.join(self.SPEEDS[1:])}"
        
        self.speed = self.SPEEDS.index(speed_level)
        if self.speed > self.SPEED_INDEX_OFF:
            self.state = self.STATE_ON
        else:
            # Technically setting speed to OFF should use turn_off, but handle it here
            self.state = self.STATE_OFF
        
        speed_str = self.SPEEDS[self.speed]
        return f"The {self.name} speed is set to {speed_str}."
    
    def get_status(self):
        """Return the current status of the fan."""
        if self.state == self.STATE_OFF:
            return f"{self.name}: {self.state}"
        return f"{self.name}: {self.state} (Speed: {self.SPEEDS[self.speed]})"


class Thermostat:
    """Simulates a smart thermostat that can adjust temperature."""
    
    # Use constants from config
    MIN_TEMP = config.THERMOSTAT_MIN_TEMP
    MAX_TEMP = config.THERMOSTAT_MAX_TEMP
    DEFAULT_ADJUST_AMOUNT = config.THERMOSTAT_DEFAULT_ADJUST_AMOUNT
    
    def __init__(self, name=config.DEFAULT_THERMOSTAT_NAME, initial_temp=config.THERMOSTAT_DEFAULT_TEMP):
        """
        Initialize a thermostat with a default name and temperature.
        
        Args:
            name (str): Name of the thermostat
            initial_temp (int): Initial temperature in Celsius (default: 22°C)
        """
        self.name = name
        self.temperature = max(min(initial_temp, self.MAX_TEMP), self.MIN_TEMP)
    
    def set_temperature(self, temp):
        """
        Set the thermostat temperature within allowed range.
        
        Args:
            temp (int/float): Desired temperature in Celsius
        
        Returns:
            str: Confirmation message
        """
        try:
            temp = float(temp)
            if temp < self.MIN_TEMP:
                self.temperature = self.MIN_TEMP
                return f"Temperature set to minimum: {self.MIN_TEMP}°C"
            elif temp > self.MAX_TEMP:
                self.temperature = self.MAX_TEMP
                return f"Temperature set to maximum: {self.MAX_TEMP}°C"
            else:
                self.temperature = temp
                return f"The {self.name} is set to {self.temperature}°C."
        except ValueError:
            return "Please provide a valid temperature value."
    
    def increase_temperature(self, amount=DEFAULT_ADJUST_AMOUNT):
        """
        Increase the temperature by the specified amount.
        
        Args:
            amount (int/float): Amount to increase temperature by (default: 1°C)
        
        Returns:
            str: Confirmation message
        """
        return self.set_temperature(self.temperature + amount)
    
    def decrease_temperature(self, amount=DEFAULT_ADJUST_AMOUNT):
        """
        Decrease the temperature by the specified amount.
        
        Args:
            amount (int/float): Amount to decrease temperature by (default: 1°C)
        
        Returns:
            str: Confirmation message
        """
        return self.set_temperature(self.temperature - amount)
    
    def get_status(self):
        """Return the current status of the thermostat."""
        return f"{self.name}: {self.temperature}°C"
