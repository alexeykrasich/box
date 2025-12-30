from .base import BaseAutomation
from typing import Dict, Any, List
import time
import requests
from datetime import datetime


class NewsMonitorAutomation(BaseAutomation):
    """Automation for monitoring news websites and sending notifications"""
    
    def get_name(self) -> str:
        return "News Monitor"
    
    def get_description(self) -> str:
        return "Monitors news websites for updates and sends notifications"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "url",
                "label": "News Website URL",
                "type": "text",
                "required": True
            },
            {
                "key": "keywords",
                "label": "Keywords to Monitor (comma-separated)",
                "type": "text",
                "required": False,
                "default": ""
            },
            {
                "key": "check_interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "600"
            },
            {
                "key": "notification_method",
                "label": "Notification Method",
                "type": "select",
                "options": ["console", "email", "push"],
                "required": False,
                "default": "console"
            }
        ]
    
    def run(self):
        """Main execution logic"""
        url = self.config.get('url')
        keywords = self.config.get('keywords', '').split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        check_interval = int(self.config.get('check_interval', 600))
        notification_method = self.config.get('notification_method', 'console')
        
        print(f"Starting news monitoring for: {url}")
        if keywords:
            print(f"Monitoring keywords: {', '.join(keywords)}")
        
        last_content_hash = None
        
        while not self.stop_flag.is_set():
            try:
                # Fetch the news page
                print(f"Checking news at {url}...")
                response = requests.get(url, timeout=10)
                content = response.text
                
                # Simple hash to detect changes
                current_hash = hash(content)
                
                if last_content_hash is None:
                    last_content_hash = current_hash
                    print("Initial content captured")
                elif current_hash != last_content_hash:
                    print("News content changed!")
                    
                    # Check for keywords if specified
                    if keywords:
                        found_keywords = [kw for kw in keywords if kw.lower() in content.lower()]
                        if found_keywords:
                            self.send_notification(
                                f"Keywords found: {', '.join(found_keywords)}",
                                notification_method
                            )
                    else:
                        self.send_notification("News content updated", notification_method)
                    
                    last_content_hash = current_hash
                
                # Wait for the specified interval or until stop is requested
                self.stop_flag.wait(check_interval)
                
            except Exception as e:
                print(f"Error monitoring news: {e}")
                self.stop_flag.wait(60)  # Wait a minute before retrying
    
    def send_notification(self, message: str, method: str):
        """Send notification using specified method"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if method == "console":
            print(f"[NOTIFICATION {timestamp}] {message}")
        elif method == "email":
            # Implement email notification
            print(f"[EMAIL NOTIFICATION {timestamp}] {message}")
            # Example: send_email(message)
        elif method == "push":
            # Implement push notification
            print(f"[PUSH NOTIFICATION {timestamp}] {message}")
            # Example: send_push_notification(message)

