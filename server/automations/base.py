from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import threading
import uuid


class AutomationStatus:
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"
    SCHEDULED = "scheduled"


class BaseAutomation(ABC):
    """Base class for all automations"""
    
    def __init__(self, automation_id: str = None):
        self.id = automation_id or str(uuid.uuid4())
        self.status = AutomationStatus.STOPPED
        self.config = {}
        self.last_run = None
        self.error_message = None
        self.thread = None
        self.stop_flag = threading.Event()
        self.status_callback = None
        
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this automation"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return description of this automation"""
        pass
    
    @abstractmethod
    def get_config_schema(self) -> List[Dict[str, Any]]:
        """
        Return configuration schema for this automation
        Format: [
            {
                "key": "field_name",
                "label": "Field Label",
                "type": "text|number|datetime|time_range",
                "required": True/False,
                "default": "default_value"
            }
        ]
        """
        pass
    
    @abstractmethod
    def run(self):
        """Main execution logic - should check self.stop_flag periodically"""
        pass
    
    def start(self, config: Dict[str, Any]):
        """Start the automation with given config"""
        if self.status == AutomationStatus.RUNNING:
            raise Exception("Automation is already running")
        
        self.config = config
        self.stop_flag.clear()
        self.status = AutomationStatus.RUNNING
        self.error_message = None
        
        self.thread = threading.Thread(target=self._run_wrapper)
        self.thread.daemon = True
        self.thread.start()
        
        self._notify_status_change()
    
    def stop(self):
        """Stop the automation"""
        if self.status != AutomationStatus.RUNNING:
            return
        
        self.stop_flag.set()
        if self.thread:
            self.thread.join(timeout=5)
        
        self.status = AutomationStatus.STOPPED
        self._notify_status_change()
    
    def _run_wrapper(self):
        """Wrapper to catch exceptions"""
        try:
            self.last_run = datetime.now().isoformat()
            self.run()
            if self.status == AutomationStatus.RUNNING:
                self.status = AutomationStatus.STOPPED
        except Exception as e:
            self.status = AutomationStatus.ERROR
            self.error_message = str(e)
        finally:
            self._notify_status_change()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "id": self.id,
            "name": self.get_name(),
            "description": self.get_description(),
            "status": self.status,
            "config": self.config,
            "last_run": self.last_run,
            "error_message": self.error_message
        }
    
    def set_status_callback(self, callback):
        """Set callback for status changes"""
        self.status_callback = callback
    
    def _notify_status_change(self):
        """Notify about status change"""
        if self.status_callback:
            self.status_callback(self.get_status())

