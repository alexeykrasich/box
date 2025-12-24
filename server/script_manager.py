"""
Script Manager - Auto-discovers and runs scripts from the scripts/ directory
"""
import os
import subprocess
import threading
import uuid
from typing import Dict, List, Any
from datetime import datetime


class ScriptManager:
    """Manages scripts in the scripts/ directory"""
    
    SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
    ALLOWED_EXTENSIONS = {'.py', '.sh', '.bash'}
    
    def __init__(self):
        self.running_scripts: Dict[str, Dict[str, Any]] = {}
        self.script_history: List[Dict[str, Any]] = []
        self._ensure_scripts_dir()
    
    def _ensure_scripts_dir(self):
        """Create scripts directory if it doesn't exist"""
        if not os.path.exists(self.SCRIPTS_DIR):
            os.makedirs(self.SCRIPTS_DIR)
    
    def list_scripts(self) -> List[Dict[str, Any]]:
        """List all available scripts"""
        scripts = []
        self._ensure_scripts_dir()
        
        for filename in os.listdir(self.SCRIPTS_DIR):
            filepath = os.path.join(self.SCRIPTS_DIR, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.ALLOWED_EXTENSIONS:
                    # Check if script is currently running
                    is_running = any(
                        s['filename'] == filename and s['status'] == 'running'
                        for s in self.running_scripts.values()
                    )
                    scripts.append({
                        'filename': filename,
                        'path': filepath,
                        'extension': ext,
                        'size': os.path.getsize(filepath),
                        'modified': datetime.fromtimestamp(
                            os.path.getmtime(filepath)
                        ).isoformat(),
                        'is_running': is_running
                    })
        
        return sorted(scripts, key=lambda x: x['filename'])
    
    def run_script(self, filename: str) -> Dict[str, Any]:
        """Run a script and return execution info"""
        filepath = os.path.join(self.SCRIPTS_DIR, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Script not found: {filename}")
        
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported script type: {ext}")
        
        run_id = str(uuid.uuid4())[:8]
        
        # Determine how to run the script
        if ext == '.py':
            cmd = ['python3', filepath]
        elif ext in {'.sh', '.bash'}:
            cmd = ['bash', filepath]
        else:
            raise ValueError(f"Unknown extension: {ext}")
        
        # Create execution record
        execution = {
            'id': run_id,
            'filename': filename,
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'output': '',
            'error': '',
            'return_code': None,
            'process': None
        }
        self.running_scripts[run_id] = execution
        
        # Run in background thread
        def run_in_thread():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self.SCRIPTS_DIR
                )
                execution['process'] = process
                stdout, stderr = process.communicate()
                
                execution['output'] = stdout.decode('utf-8', errors='replace')
                execution['error'] = stderr.decode('utf-8', errors='replace')
                execution['return_code'] = process.returncode
                execution['status'] = 'completed' if process.returncode == 0 else 'failed'
                execution['finished_at'] = datetime.now().isoformat()
            except Exception as e:
                execution['status'] = 'error'
                execution['error'] = str(e)
                execution['finished_at'] = datetime.now().isoformat()
            finally:
                execution['process'] = None
                self.script_history.append(execution.copy())
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        
        return {'id': run_id, 'filename': filename, 'status': 'running'}
    
    def get_script_status(self, run_id: str) -> Dict[str, Any]:
        """Get status of a running/completed script"""
        if run_id in self.running_scripts:
            exec_info = self.running_scripts[run_id].copy()
            exec_info.pop('process', None)  # Don't serialize process
            return exec_info
        raise ValueError(f"Script execution not found: {run_id}")
    
    def stop_script(self, run_id: str) -> Dict[str, Any]:
        """Stop a running script"""
        if run_id not in self.running_scripts:
            raise ValueError(f"Script execution not found: {run_id}")
        
        execution = self.running_scripts[run_id]
        if execution['process'] and execution['status'] == 'running':
            execution['process'].terminate()
            execution['status'] = 'stopped'
            execution['finished_at'] = datetime.now().isoformat()
        
        result = execution.copy()
        result.pop('process', None)
        return result
    
    def get_running_scripts(self) -> List[Dict[str, Any]]:
        """Get all currently running scripts"""
        running = []
        for run_id, exec_info in self.running_scripts.items():
            if exec_info['status'] == 'running':
                info = exec_info.copy()
                info.pop('process', None)
                running.append(info)
        return running

