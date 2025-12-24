"""
Docker Manager - Manage Docker containers from the API
"""
import subprocess
import json
from typing import Dict, List, Any, Optional


class DockerManager:
    """Manages Docker containers via docker CLI"""
    
    def __init__(self):
        self._check_docker_available()
    
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
        """Run a docker command and return result"""
        try:
            result = subprocess.run(
                ['docker'] + args,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result
        except subprocess.TimeoutExpired as e:
            raise Exception(f"Docker command timed out: {' '.join(args)}")
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
        result = self._run_docker_command(['start', container_id])
        
        if result.returncode != 0:
            raise Exception(f"Failed to start container: {result.stderr}")
        
        return {
            'success': True,
            'container_id': container_id,
            'action': 'started',
            'message': f"Container {container_id} started successfully"
        }
    
    def stop_container(self, container_id: str) -> Dict[str, Any]:
        """Stop a running container"""
        result = self._run_docker_command(['stop', container_id])
        
        if result.returncode != 0:
            raise Exception(f"Failed to stop container: {result.stderr}")
        
        return {
            'success': True,
            'container_id': container_id,
            'action': 'stopped',
            'message': f"Container {container_id} stopped successfully"
        }
    
    def restart_container(self, container_id: str) -> Dict[str, Any]:
        """Restart a container"""
        result = self._run_docker_command(['restart', container_id])
        
        if result.returncode != 0:
            raise Exception(f"Failed to restart container: {result.stderr}")
        
        return {
            'success': True,
            'container_id': container_id,
            'action': 'restarted',
            'message': f"Container {container_id} restarted successfully"
        }
    
    def get_container_logs(self, container_id: str, tail: int = 100) -> Dict[str, Any]:
        """Get container logs"""
        result = self._run_docker_command(['logs', '--tail', str(tail), container_id])
        
        # Docker logs can output to both stdout and stderr
        return {
            'container_id': container_id,
            'logs': result.stdout + result.stderr,
            'success': result.returncode == 0
        }
    
    def get_container_info(self, container_id: str) -> Dict[str, Any]:
        """Get detailed container information"""
        result = self._run_docker_command(['inspect', container_id])
        
        if result.returncode != 0:
            raise Exception(f"Failed to inspect container: {result.stderr}")
        
        try:
            info = json.loads(result.stdout)
            if info:
                return info[0]
        except json.JSONDecodeError:
            raise Exception("Failed to parse container info")
        
        return {}
    
    def is_docker_available(self) -> bool:
        """Check if Docker daemon is running"""
        return self._check_docker_available()

