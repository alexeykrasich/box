from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from automation_manager import AutomationManager
from script_manager import ScriptManager
from docker_manager import DockerManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Managers
manager = AutomationManager()
script_manager = ScriptManager()
docker_manager = DockerManager()


def broadcast_status_update(status):
    """Broadcast status update via WebSocket"""
    socketio.emit('status_update', status, broadcast=True)


# Set status callback
manager.set_status_callback(broadcast_status_update)


# REST API Endpoints

@app.route('/api/automations/types', methods=['GET'])
def get_automation_types():
    """Get available automation types"""
    try:
        types = manager.get_available_automations()
        return jsonify({"success": True, "data": types})
    except Exception as e:
        logger.error(f"Error getting automation types: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/automations', methods=['GET'])
def list_automations():
    """List all automation instances"""
    try:
        automations = manager.list_automations()
        return jsonify({"success": True, "data": automations})
    except Exception as e:
        logger.error(f"Error listing automations: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/automations', methods=['POST'])
def create_automation():
    """Create a new automation instance"""
    try:
        data = request.json
        automation_type = data.get('type')
        
        if not automation_type:
            return jsonify({"success": False, "error": "Missing automation type"}), 400
        
        automation = manager.create_automation(automation_type)
        return jsonify({"success": True, "data": automation}), 201
    except Exception as e:
        logger.error(f"Error creating automation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/automations/<automation_id>', methods=['GET'])
def get_automation_status(automation_id):
    """Get automation status"""
    try:
        status = manager.get_status(automation_id)
        return jsonify({"success": True, "data": status})
    except Exception as e:
        logger.error(f"Error getting automation status: {e}")
        return jsonify({"success": False, "error": str(e)}), 404


@app.route('/api/automations/<automation_id>/start', methods=['POST'])
def start_automation(automation_id):
    """Start an automation"""
    try:
        data = request.json
        config = data.get('config', {})
        
        status = manager.start_automation(automation_id, config)
        return jsonify({"success": True, "data": status})
    except Exception as e:
        logger.error(f"Error starting automation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/automations/<automation_id>/stop', methods=['POST'])
def stop_automation(automation_id):
    """Stop an automation"""
    try:
        status = manager.stop_automation(automation_id)
        return jsonify({"success": True, "data": status})
    except Exception as e:
        logger.error(f"Error stopping automation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/automations/<automation_id>', methods=['DELETE'])
def delete_automation(automation_id):
    """Delete an automation"""
    try:
        manager.delete_automation(automation_id)
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error deleting automation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# ============== SCRIPTS API ==============

@app.route('/api/scripts', methods=['GET'])
def list_scripts():
    """List all available scripts in scripts/ directory"""
    try:
        scripts = script_manager.list_scripts()
        return jsonify({"success": True, "data": scripts})
    except Exception as e:
        logger.error(f"Error listing scripts: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/scripts/<filename>/run', methods=['POST'])
def run_script(filename):
    """Run a script by filename"""
    try:
        result = script_manager.run_script(filename)
        return jsonify({"success": True, "data": result})
    except FileNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error running script: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/scripts/running', methods=['GET'])
def get_running_scripts():
    """Get all currently running scripts"""
    try:
        scripts = script_manager.get_running_scripts()
        return jsonify({"success": True, "data": scripts})
    except Exception as e:
        logger.error(f"Error getting running scripts: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/scripts/status/<run_id>', methods=['GET'])
def get_script_status(run_id):
    """Get status of a script execution"""
    try:
        status = script_manager.get_script_status(run_id)
        return jsonify({"success": True, "data": status})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting script status: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/scripts/stop/<run_id>', methods=['POST'])
def stop_script(run_id):
    """Stop a running script"""
    try:
        result = script_manager.stop_script(run_id)
        return jsonify({"success": True, "data": result})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error stopping script: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============== DOCKER API ==============

@app.route('/api/docker/status', methods=['GET'])
def docker_status():
    """Check if Docker is available"""
    try:
        available = docker_manager.is_docker_available()
        return jsonify({"success": True, "data": {"available": available}})
    except Exception as e:
        return jsonify({"success": True, "data": {"available": False, "error": str(e)}})


@app.route('/api/docker/containers', methods=['GET'])
def list_containers():
    """List all Docker containers"""
    try:
        all_containers = request.args.get('all', 'true').lower() == 'true'
        containers = docker_manager.list_containers(all_containers)
        return jsonify({"success": True, "data": containers})
    except Exception as e:
        logger.error(f"Error listing containers: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/docker/containers/<container_id>/start', methods=['POST'])
def start_container(container_id):
    """Start a Docker container"""
    try:
        result = docker_manager.start_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error starting container: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/docker/containers/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    """Stop a Docker container"""
    try:
        result = docker_manager.stop_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error stopping container: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/docker/containers/<container_id>/restart', methods=['POST'])
def restart_container(container_id):
    """Restart a Docker container"""
    try:
        result = docker_manager.restart_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error restarting container: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/docker/containers/<container_id>/logs', methods=['GET'])
def get_container_logs(container_id):
    """Get container logs"""
    try:
        tail = int(request.args.get('tail', 100))
        result = docker_manager.get_container_logs(container_id, tail)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error getting container logs: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# WebSocket Events

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connected', {'message': 'Connected to automation server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


@socketio.on('request_status')
def handle_status_request(data):
    """Handle status request"""
    try:
        automation_id = data.get('automation_id')
        if automation_id:
            status = manager.get_status(automation_id)
            emit('status_update', status)
        else:
            statuses = manager.list_automations()
            emit('status_update', statuses)
    except Exception as e:
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    logger.info("Starting Automation Server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

