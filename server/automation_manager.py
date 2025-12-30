from typing import Dict, List, Any
from automations import AVAILABLE_AUTOMATIONS
from automations.base import BaseAutomation


class AutomationManager:
    """Manages all automation instances"""
    
    def __init__(self):
        self.automations: Dict[str, BaseAutomation] = {}
        self.automation_classes = {cls.__name__: cls for cls in AVAILABLE_AUTOMATIONS}
        self.status_callback = None
    
    def set_status_callback(self, callback):
        """Set callback for status updates"""
        self.status_callback = callback
    
    def get_available_automations(self) -> List[Dict[str, Any]]:
        """Get list of available automation types"""
        result = []
        for class_name, automation_class in self.automation_classes.items():
            instance = automation_class()
            result.append({
                "type": class_name,
                "name": instance.get_name(),
                "description": instance.get_description(),
                "config_schema": instance.get_config_schema()
            })
        return result
    
    def create_automation(self, automation_type: str) -> Dict[str, Any]:
        """Create a new automation instance"""
        if automation_type not in self.automation_classes:
            raise ValueError(f"Unknown automation type: {automation_type}")
        
        automation_class = self.automation_classes[automation_type]
        automation = automation_class()
        
        # Set status callback
        if self.status_callback:
            automation.set_status_callback(self.status_callback)
        
        self.automations[automation.id] = automation
        return automation.get_status()
    
    def get_automation(self, automation_id: str) -> BaseAutomation:
        """Get automation by ID"""
        if automation_id not in self.automations:
            raise ValueError(f"Automation not found: {automation_id}")
        return self.automations[automation_id]
    
    def list_automations(self) -> List[Dict[str, Any]]:
        """List all automation instances"""
        return [auto.get_status() for auto in self.automations.values()]
    
    def start_automation(self, automation_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Start an automation with config"""
        automation = self.get_automation(automation_id)
        automation.start(config)
        return automation.get_status()
    
    def stop_automation(self, automation_id: str) -> Dict[str, Any]:
        """Stop an automation"""
        automation = self.get_automation(automation_id)
        automation.stop()
        return automation.get_status()
    
    def get_status(self, automation_id: str) -> Dict[str, Any]:
        """Get automation status"""
        automation = self.get_automation(automation_id)
        return automation.get_status()
    
    def delete_automation(self, automation_id: str):
        """Delete an automation instance"""
        automation = self.get_automation(automation_id)
        if automation.status == "running":
            automation.stop()
        del self.automations[automation_id]
    
    def stop_all(self):
        """Stop all running automations"""
        for automation in self.automations.values():
            if automation.status == "running":
                automation.stop()

