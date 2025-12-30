"""
Docker Manager - Manage Docker containers from the API
Secured against command injection attacks.
"""
import subprocess
import json
import re
from typing import Dict, List, Any


# Pattern for valid container IDs (alphanumeric, dash, underscore, dot)
CONTAINER_ID_PATTERN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}$')


def _validate_container_id(container_id: str) -> bool:
    """Validate container ID to prevent command injection"""
    if not container_id or not isinstance(container_id, str):
        return False
    return bool(CONTAINER_ID_PATTERN.match(container_id))


class DockerManager:
    """Manages Docker containers via docker CLI"""

    def __init__(self):
        self._docker_available = self._check_docker_available()

    def _check_docker_available(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ['docker', 'version', '--format', '{{.Server.Version}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _run_docker_command(self, args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """Run a docker command and return result. Uses list args to prevent shell injection."""
        try:
            # Never use shell=True to prevent command injection
            result = subprocess.run(
                ['docker'] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False  # Explicit: prevent shell injection
            )
            return result
        except subprocess.TimeoutExpired:
            raise Exception("Docker command timed out")
        except FileNotFoundError:
            raise Exception("Docker is not installed or not in PATH")
    
    def list_containers(self, all_containers: bool = True) -> List[Dict[str, Any]]:
        """List all Docker containers"""
        args = ['ps', '--format', '{{json .}}']
        if all_containers:
            args.insert(1, '-a')
        
        result = self._run_docker_command(args)
        
        if result.returncode != 0:
            raise Exception(f"Failed to list containers: {result.stderr}")
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    container = json.loads(line)
                    containers.append({
                        'id': container.get('ID', ''),
                        'name': container.get('Names', ''),
                        'image': container.get('Image', ''),
                        'status': container.get('Status', ''),
                        'state': container.get('State', ''),
                        'ports': container.get('Ports', ''),
                        'created': container.get('CreatedAt', ''),
                        'is_running': container.get('State', '').lower() == 'running'
                    })
                except json.JSONDecodeError:
                    continue
        
        return containers
    
    def start_container(self, container_id: str) -> Dict[str, Any]:
        """Start a stopped container"""
        if not _validate_container_id(container_id):
            raise ValueError("Invalid container ID")

        result = self._run_docker_command(['start', container_id])

        if result.returncode != 0:
            raise Exception("Failed to start container")

        return {
            'success': True,
            'container_id': container_id,
            'action': 'started'
        }

    def stop_container(self, container_id: str) -> Dict[str, Any]:
        """Stop a running container"""
        if not _validate_container_id(container_id):
            raise ValueError("Invalid container ID")

        result = self._run_docker_command(['stop', container_id])

        if result.returncode != 0:
            raise Exception("Failed to stop container")

        return {
            'success': True,
            'container_id': container_id,
            'action': 'stopped'
        }

    def restart_container(self, container_id: str) -> Dict[str, Any]:
        """Restart a container"""
        if not _validate_container_id(container_id):
            raise ValueError("Invalid container ID")

        result = self._run_docker_command(['restart', container_id])

        if result.returncode != 0:
            raise Exception("Failed to restart container")

        return {
            'success': True,
            'container_id': container_id,
            'action': 'restarted'
        }

    def get_container_logs(self, container_id: str, tail: int = 100) -> Dict[str, Any]:
        """Get container logs"""
        if not _validate_container_id(container_id):
            raise ValueError("Invalid container ID")

        # Sanitize tail value
        tail = max(1, min(int(tail), 10000))

        result = self._run_docker_command(['logs', '--tail', str(tail), container_id])

        return {
            'container_id': container_id,
            'logs': result.stdout + result.stderr,
            'success': result.returncode == 0
        }

    def get_container_info(self, container_id: str) -> Dict[str, Any]:
        """Get detailed container information"""
        if not _validate_container_id(container_id):
            raise ValueError("Invalid container ID")

        result = self._run_docker_command(['inspect', container_id])

        if result.returncode != 0:
            raise Exception("Failed to inspect container")

        try:
            info = json.loads(result.stdout)
            if info:
                return info[0]
        except json.JSONDecodeError:
            raise Exception("Failed to parse container info")

        return {}

    def is_docker_available(self) -> bool:
        """Check if Docker daemon is running"""
        return self._docker_available or self._check_docker_available()

