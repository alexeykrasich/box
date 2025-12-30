"""
Script Manager - Auto-discovers and runs scripts from the scripts/ directory
Secured against path traversal and command injection attacks.
"""
import os
import subprocess
import threading
import uuid
import re
from typing import Dict, List, Any
from datetime import datetime


# Strict filename pattern - alphanumeric, underscore, dash, dot only
FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')


def _validate_filename(filename: str) -> bool:
    """Validate filename to prevent path traversal"""
    if not filename or not isinstance(filename, str):
        return False
    # Block path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    if not FILENAME_PATTERN.match(filename):
        return False
    return len(filename) <= 255


class ScriptManager:
    """Manages scripts in the scripts/ directory"""

    SCRIPTS_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'scripts'))
    ALLOWED_EXTENSIONS = frozenset({'.py', '.sh', '.bash'})
    MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB max output

    def __init__(self):
        self.running_scripts: Dict[str, Dict[str, Any]] = {}
        self.script_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._ensure_scripts_dir()

    def _ensure_scripts_dir(self):
        """Create scripts directory if it doesn't exist"""
        if not os.path.exists(self.SCRIPTS_DIR):
            os.makedirs(self.SCRIPTS_DIR, mode=0o755)
    
    def list_scripts(self) -> List[Dict[str, Any]]:
        """List all available scripts"""
        scripts = []
        self._ensure_scripts_dir()

        for filename in os.listdir(self.SCRIPTS_DIR):
            # Validate filename
            if not _validate_filename(filename):
                continue

            filepath = os.path.join(self.SCRIPTS_DIR, filename)
            # Ensure path is within scripts directory (prevent symlink attacks)
            if not os.path.realpath(filepath).startswith(self.SCRIPTS_DIR):
                continue

            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.ALLOWED_EXTENSIONS:
                    with self._lock:
                        is_running = any(
                            s['filename'] == filename and s['status'] == 'running'
                            for s in self.running_scripts.values()
                        )
                    scripts.append({
                        'filename': filename,
                        'extension': ext,
                        'size': os.path.getsize(filepath),
                        'modified': datetime.fromtimestamp(
                            os.path.getmtime(filepath)
                        ).isoformat(),
                        'is_running': is_running
                    })

        return sorted(scripts, key=lambda x: x['filename'])

    def _validate_script_path(self, filename: str) -> str:
        """Validate and return safe script path"""
        if not _validate_filename(filename):
            raise ValueError("Invalid filename")

        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError("Unsupported script type")

        filepath = os.path.join(self.SCRIPTS_DIR, filename)
        realpath = os.path.realpath(filepath)

        # Prevent path traversal
        if not realpath.startswith(self.SCRIPTS_DIR):
            raise ValueError("Invalid script path")

        if not os.path.isfile(realpath):
            raise FileNotFoundError("Script not found")

        return realpath

    def run_script(self, filename: str) -> Dict[str, Any]:
        """Run a script and return execution info"""
        filepath = self._validate_script_path(filename)
        ext = os.path.splitext(filename)[1].lower()

        run_id = str(uuid.uuid4())[:8]

        # Determine how to run the script - use absolute paths
        if ext == '.py':
            cmd = ['python3', filepath]
        elif ext in {'.sh', '.bash'}:
            cmd = ['bash', filepath]
        else:
            raise ValueError("Unknown extension")

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

        with self._lock:
            self.running_scripts[run_id] = execution

        # Run in background thread
        def run_in_thread():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self.SCRIPTS_DIR,
                    shell=False  # Prevent shell injection
                )
                execution['process'] = process
                stdout, stderr = process.communicate(timeout=3600)  # 1 hour timeout

                # Limit output size
                execution['output'] = stdout.decode('utf-8', errors='replace')[:self.MAX_OUTPUT_SIZE]
                execution['error'] = stderr.decode('utf-8', errors='replace')[:self.MAX_OUTPUT_SIZE]
                execution['return_code'] = process.returncode
                execution['status'] = 'completed' if process.returncode == 0 else 'failed'
                execution['finished_at'] = datetime.now().isoformat()
            except subprocess.TimeoutExpired:
                execution['status'] = 'timeout'
                execution['error'] = 'Script execution timed out'
                execution['finished_at'] = datetime.now().isoformat()
                if execution['process']:
                    execution['process'].kill()
            except Exception as e:
                execution['status'] = 'error'
                execution['error'] = str(e)[:1000]
                execution['finished_at'] = datetime.now().isoformat()
            finally:
                execution['process'] = None
                with self._lock:
                    # Limit history size
                    if len(self.script_history) >= 100:
                        self.script_history = self.script_history[-99:]
                    self.script_history.append(execution.copy())

        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()

        return {'id': run_id, 'filename': filename, 'status': 'running'}

    def get_script_status(self, run_id: str) -> Dict[str, Any]:
        """Get status of a running/completed script"""
        with self._lock:
            if run_id in self.running_scripts:
                exec_info = self.running_scripts[run_id].copy()
                exec_info.pop('process', None)
                return exec_info
        raise ValueError("Script execution not found")

    def stop_script(self, run_id: str) -> Dict[str, Any]:
        """Stop a running script"""
        with self._lock:
            if run_id not in self.running_scripts:
                raise ValueError("Script execution not found")

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
        with self._lock:
            running = []
            for exec_info in self.running_scripts.values():
                if exec_info['status'] == 'running':
                    info = exec_info.copy()
                    info.pop('process', None)
                    running.append(info)
            return running

