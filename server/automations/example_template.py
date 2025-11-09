"""
Template for creating new automations.
Copy this file and modify it to create your own automation.

Steps to add a new automation:
1. Copy this file to a new file (e.g., my_automation.py)
2. Rename the class (e.g., MyAutomation)
3. Implement the required methods
4. Add your automation to __init__.py in AVAILABLE_AUTOMATIONS list
5. Restart the server
"""

from .base import BaseAutomation
from typing import Dict, Any, List
import time


class ExampleAutomation(BaseAutomation):
    """
    Example automation template.
    Replace this with your automation description.
    """
    
    def get_name(self) -> str:
        """
        Return the display name of this automation.
        This will be shown in the Android app.
        """
        return "Example Automation"
    
    def get_description(self) -> str:
        """
        Return a brief description of what this automation does.
        """
        return "This is an example automation template"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        """
        Define the configuration fields for this automation.
        
        Available field types:
        - "text": Text input
        - "number": Numeric input
        - "date": Date picker (format: YYYY-MM-DD)
        - "time": Time picker (format: HH:MM)
        - "select": Dropdown (requires "options" list)
        
        Returns:
            List of configuration field definitions
        """
        return [
            {
                "key": "example_text",
                "label": "Example Text Field",
                "type": "text",
                "required": True,
                "default": "default value"
            },
            {
                "key": "example_number",
                "label": "Example Number Field",
                "type": "number",
                "required": False,
                "default": "60"
            },
            {
                "key": "example_date",
                "label": "Example Date Field",
                "type": "date",
                "required": False
            },
            {
                "key": "example_time",
                "label": "Example Time Field",
                "type": "time",
                "required": False,
                "default": "12:00"
            }
        ]
    
    def run(self):
        """
        Main execution logic for the automation.
        
        Important:
        - Access configuration values using: self.config.get('field_key')
        - Check self.stop_flag periodically to allow stopping
        - Use self.stop_flag.wait(seconds) instead of time.sleep()
        - Raise exceptions if something goes wrong (they will be caught)
        """
        # Get configuration values
        text_value = self.config.get('example_text')
        number_value = int(self.config.get('example_number', 60))
        date_value = self.config.get('example_date')
        time_value = self.config.get('example_time')
        
        print(f"Starting example automation with config:")
        print(f"  Text: {text_value}")
        print(f"  Number: {number_value}")
        print(f"  Date: {date_value}")
        print(f"  Time: {time_value}")
        
        # Main loop - runs until stopped
        iteration = 0
        while not self.stop_flag.is_set():
            iteration += 1
            
            # Your automation logic here
            print(f"Example automation running... iteration {iteration}")
            
            # Example: Do some work
            # result = do_something(text_value)
            # if result:
            #     print(f"Success: {result}")
            
            # Wait before next iteration
            # Use self.stop_flag.wait() instead of time.sleep()
            # This allows the automation to stop immediately when requested
            self.stop_flag.wait(number_value)
        
        print("Example automation stopped")


# Example of a more complex automation
class AdvancedExampleAutomation(BaseAutomation):
    """Example of a more complex automation with error handling"""
    
    def get_name(self) -> str:
        return "Advanced Example"
    
    def get_description(self) -> str:
        return "Advanced automation with error handling and state"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "url",
                "label": "URL to Monitor",
                "type": "text",
                "required": True
            },
            {
                "key": "interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "300"
            }
        ]
    
    def run(self):
        url = self.config.get('url')
        interval = int(self.config.get('interval', 300))
        
        print(f"Monitoring {url} every {interval} seconds")
        
        while not self.stop_flag.is_set():
            try:
                # Your logic here
                print(f"Checking {url}...")
                
                # Example: Make HTTP request
                # import requests
                # response = requests.get(url, timeout=10)
                # if response.status_code == 200:
                #     print("URL is accessible")
                
            except Exception as e:
                # Handle errors gracefully
                print(f"Error: {e}")
                # Continue running despite errors
            
            # Wait for next iteration
            self.stop_flag.wait(interval)

