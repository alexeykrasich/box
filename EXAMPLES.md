# Automation Examples

This document provides real-world examples of automations you can build.

## Example 1: Price Tracker

Monitor product prices and get notified when price drops.

```python
# server/automations/price_tracker.py

from .base import BaseAutomation
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup

class PriceTrackerAutomation(BaseAutomation):
    
    def get_name(self) -> str:
        return "Price Tracker"
    
    def get_description(self) -> str:
        return "Monitor product prices and notify on price drops"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "product_url",
                "label": "Product URL",
                "type": "text",
                "required": True
            },
            {
                "key": "target_price",
                "label": "Target Price",
                "type": "number",
                "required": True
            },
            {
                "key": "check_interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "3600"  # 1 hour
            }
        ]
    
    def run(self):
        url = self.config.get('product_url')
        target_price = float(self.config.get('target_price'))
        interval = int(self.config.get('check_interval', 3600))
        
        print(f"Tracking price for: {url}")
        print(f"Target price: ${target_price}")
        
        while not self.stop_flag.is_set():
            try:
                # Fetch the page
                response = requests.get(url, timeout=10)
                current_price = self.extract_price(response.text)
                
                if current_price:
                    print(f"Current price: ${current_price}")
                    
                    if current_price <= target_price:
                        print(f"🎉 PRICE DROP! ${current_price} <= ${target_price}")
                        # Send notification here
                        # self.send_notification(f"Price dropped to ${current_price}!")
                else:
                    print("Could not extract price")
                    
            except Exception as e:
                print(f"Error checking price: {e}")
            
            self.stop_flag.wait(interval)
    
    def extract_price(self, html: str) -> float:
        """
        Extract price from HTML.
        Customize this based on the website structure.
        """
        # Example: Look for common price patterns
        import re
        
        # Try to find price patterns like $99.99 or 99.99
        patterns = [
            r'\$(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*USD',
            r'price["\s:]+(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return None
```

## Example 2: Website Uptime Monitor

Check if your website is up and get notified on downtime.

```python
# server/automations/uptime_monitor.py

from .base import BaseAutomation
from typing import Dict, Any, List
import requests
from datetime import datetime

class UptimeMonitorAutomation(BaseAutomation):
    
    def get_name(self) -> str:
        return "Uptime Monitor"
    
    def get_description(self) -> str:
        return "Monitor website uptime and alert on downtime"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "url",
                "label": "Website URL",
                "type": "text",
                "required": True
            },
            {
                "key": "check_interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "300"  # 5 minutes
            },
            {
                "key": "timeout",
                "label": "Request Timeout (seconds)",
                "type": "number",
                "required": False,
                "default": "10"
            }
        ]
    
    def run(self):
        url = self.config.get('url')
        interval = int(self.config.get('check_interval', 300))
        timeout = int(self.config.get('timeout', 10))
        
        consecutive_failures = 0
        last_status = "unknown"
        
        print(f"Monitoring uptime for: {url}")
        
        while not self.stop_flag.is_set():
            try:
                start_time = datetime.now()
                response = requests.get(url, timeout=timeout)
                response_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    if last_status == "down":
                        print(f"✅ WEBSITE IS BACK UP! Response time: {response_time:.2f}s")
                        # Send recovery notification
                    
                    print(f"✓ Website is up (Status: {response.status_code}, Time: {response_time:.2f}s)")
                    consecutive_failures = 0
                    last_status = "up"
                else:
                    consecutive_failures += 1
                    print(f"⚠ Unexpected status code: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                consecutive_failures += 1
                print(f"⚠ Request timeout after {timeout}s")
                
            except Exception as e:
                consecutive_failures += 1
                print(f"❌ Error: {e}")
            
            # Alert after 3 consecutive failures
            if consecutive_failures >= 3 and last_status != "down":
                print(f"🚨 WEBSITE IS DOWN! ({consecutive_failures} consecutive failures)")
                last_status = "down"
                # Send alert notification
            
            self.stop_flag.wait(interval)
```

## Example 3: Social Media Monitor

Monitor social media for mentions or hashtags.

```python
# server/automations/social_monitor.py

from .base import BaseAutomation
from typing import Dict, Any, List
import requests

class SocialMediaMonitorAutomation(BaseAutomation):
    
    def get_name(self) -> str:
        return "Social Media Monitor"
    
    def get_description(self) -> str:
        return "Monitor social media for keywords and hashtags"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "platform",
                "label": "Platform",
                "type": "select",
                "options": ["twitter", "reddit", "hackernews"],
                "required": True,
                "default": "reddit"
            },
            {
                "key": "keywords",
                "label": "Keywords (comma-separated)",
                "type": "text",
                "required": True
            },
            {
                "key": "check_interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "600"
            }
        ]
    
    def run(self):
        platform = self.config.get('platform')
        keywords = [k.strip() for k in self.config.get('keywords', '').split(',')]
        interval = int(self.config.get('check_interval', 600))
        
        print(f"Monitoring {platform} for keywords: {', '.join(keywords)}")
        
        seen_posts = set()
        
        while not self.stop_flag.is_set():
            try:
                if platform == "reddit":
                    new_posts = self.check_reddit(keywords, seen_posts)
                elif platform == "hackernews":
                    new_posts = self.check_hackernews(keywords, seen_posts)
                # Add more platforms as needed
                
                for post in new_posts:
                    print(f"📱 New mention: {post['title']}")
                    print(f"   URL: {post['url']}")
                    # Send notification
                    
            except Exception as e:
                print(f"Error monitoring {platform}: {e}")
            
            self.stop_flag.wait(interval)
    
    def check_reddit(self, keywords, seen_posts):
        """Check Reddit for keywords"""
        new_posts = []
        
        for keyword in keywords:
            url = f"https://www.reddit.com/search.json?q={keyword}&sort=new&limit=10"
            headers = {'User-Agent': 'AutomationBot/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_id = post['data']['id']
                if post_id not in seen_posts:
                    seen_posts.add(post_id)
                    new_posts.append({
                        'title': post['data']['title'],
                        'url': f"https://reddit.com{post['data']['permalink']}"
                    })
        
        return new_posts
    
    def check_hackernews(self, keywords, seen_posts):
        """Check Hacker News for keywords"""
        # Implementation for HN API
        return []
```

## Example 4: File Backup Monitor

Monitor a directory and backup files when changes are detected.

```python
# server/automations/backup_monitor.py

from .base import BaseAutomation
from typing import Dict, Any, List
import os
import shutil
from datetime import datetime
import hashlib

class BackupMonitorAutomation(BaseAutomation):
    
    def get_name(self) -> str:
        return "File Backup Monitor"
    
    def get_description(self) -> str:
        return "Monitor directory and backup changed files"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "source_dir",
                "label": "Source Directory",
                "type": "text",
                "required": True
            },
            {
                "key": "backup_dir",
                "label": "Backup Directory",
                "type": "text",
                "required": True
            },
            {
                "key": "check_interval",
                "label": "Check Interval (seconds)",
                "type": "number",
                "required": False,
                "default": "300"
            }
        ]
    
    def run(self):
        source = self.config.get('source_dir')
        backup = self.config.get('backup_dir')
        interval = int(self.config.get('check_interval', 300))
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup, exist_ok=True)
        
        file_hashes = {}
        
        print(f"Monitoring: {source}")
        print(f"Backing up to: {backup}")
        
        while not self.stop_flag.is_set():
            try:
                for root, dirs, files in os.walk(source):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        
                        # Calculate file hash
                        current_hash = self.get_file_hash(filepath)
                        
                        # Check if file changed
                        if filepath not in file_hashes or file_hashes[filepath] != current_hash:
                            print(f"📁 File changed: {filename}")
                            self.backup_file(filepath, source, backup)
                            file_hashes[filepath] = current_hash
                            
            except Exception as e:
                print(f"Error during backup: {e}")
            
            self.stop_flag.wait(interval)
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def backup_file(self, filepath, source_dir, backup_dir):
        """Backup a file with timestamp"""
        rel_path = os.path.relpath(filepath, source_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{timestamp}_{rel_path}")
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(filepath, backup_path)
        print(f"✓ Backed up to: {backup_path}")
```

## Registering Your Automations

After creating your automation, add it to `server/automations/__init__.py`:

```python
from .ticket_buyer import TicketBuyerAutomation
from .news_monitor import NewsMonitorAutomation
from .price_tracker import PriceTrackerAutomation
from .uptime_monitor import UptimeMonitorAutomation
from .social_monitor import SocialMediaMonitorAutomation
from .backup_monitor import BackupMonitorAutomation

AVAILABLE_AUTOMATIONS = [
    TicketBuyerAutomation,
    NewsMonitorAutomation,
    PriceTrackerAutomation,
    UptimeMonitorAutomation,
    SocialMediaMonitorAutomation,
    BackupMonitorAutomation,
]
```

Restart the server and your new automations will appear in the Android app!

