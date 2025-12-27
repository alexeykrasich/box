from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from automation_manager import AutomationManager
from script_manager import ScriptManager
from docker_manager import DockerManager
from config import (
    Config, require_api_key, rate_limit, audit_log,
    validate_input, sanitize_string
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
security_logger = logging.getLogger('security')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# CORS configuration - restrict origins in production
cors_origins = Config.CORS_ORIGINS if Config.CORS_ORIGINS != ['*'] else "*"
CORS(app, origins=cors_origins, supports_credentials=True)

# Initialize SocketIO with restricted origins
socketio = SocketIO(
    app,
    cors_allowed_origins=cors_origins if cors_origins != "*" else "*"
)

# Initialize Managers
manager = AutomationManager()
script_manager = ScriptManager()
docker_manager = DockerManager()


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    for header, value in Config.SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


def broadcast_status_update(status):
    """Broadcast status update via WebSocket"""
    socketio.emit('status_update', status, broadcast=True)


# Set status callback
manager.set_status_callback(broadcast_status_update)


# REST API Endpoints

@app.route('/api/automations/types', methods=['GET'])
@rate_limit
@require_api_key
def get_automation_types():
    """Get available automation types"""
    try:
        types = manager.get_available_automations()
        return jsonify({"success": True, "data": types})
    except Exception as e:
        logger.error(f"Error getting automation types: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations', methods=['GET'])
@rate_limit
@require_api_key
def list_automations():
    """List all automation instances"""
    try:
        automations = manager.list_automations()
        return jsonify({"success": True, "data": automations})
    except Exception as e:
        logger.error(f"Error listing automations: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations', methods=['POST'])
@rate_limit
@require_api_key
def create_automation():
    """Create a new automation instance"""
    try:
        data = request.json or {}
        automation_type = sanitize_string(data.get('type', ''))

        if not automation_type:
            return jsonify({"success": False, "error": "Missing automation type"}), 400

        if not validate_input(automation_type, 'automation_type'):
            return jsonify({"success": False, "error": "Invalid automation type format"}), 400

        audit_log("CREATE_AUTOMATION", f"type={automation_type}")
        automation = manager.create_automation(automation_type)
        return jsonify({"success": True, "data": automation}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating automation: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations/<automation_id>', methods=['GET'])
@rate_limit
@require_api_key
def get_automation_status(automation_id):
    """Get automation status"""
    try:
        if not validate_input(automation_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid automation ID format"}), 400

        status = manager.get_status(automation_id)
        return jsonify({"success": True, "data": status})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting automation status: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations/<automation_id>/start', methods=['POST'])
@rate_limit
@require_api_key
def start_automation(automation_id):
    """Start an automation"""
    try:
        if not validate_input(automation_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid automation ID format"}), 400

        data = request.json or {}
        config = data.get('config', {})

        audit_log("START_AUTOMATION", f"id={automation_id}")
        status = manager.start_automation(automation_id, config)
        return jsonify({"success": True, "data": status})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error starting automation: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations/<automation_id>/stop', methods=['POST'])
@rate_limit
@require_api_key
def stop_automation(automation_id):
    """Stop an automation"""
    try:
        if not validate_input(automation_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid automation ID format"}), 400

        audit_log("STOP_AUTOMATION", f"id={automation_id}")
        status = manager.stop_automation(automation_id)
        return jsonify({"success": True, "data": status})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error stopping automation: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/automations/<automation_id>', methods=['DELETE'])
@rate_limit
@require_api_key
def delete_automation(automation_id):
    """Delete an automation"""
    try:
        if not validate_input(automation_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid automation ID format"}), 400

        audit_log("DELETE_AUTOMATION", f"id={automation_id}")
        manager.delete_automation(automation_id)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error deleting automation: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

# ============== SCRIPTS API ==============

@app.route('/api/scripts', methods=['GET'])
@rate_limit
@require_api_key
def list_scripts():
    """List all available scripts in scripts/ directory"""
    try:
        scripts = script_manager.list_scripts()
        return jsonify({"success": True, "data": scripts})
    except Exception as e:
        logger.error(f"Error listing scripts: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/scripts/<filename>/run', methods=['POST'])
@rate_limit
@require_api_key
def run_script(filename):
    """Run a script by filename"""
    try:
        if not validate_input(filename, 'filename'):
            return jsonify({"success": False, "error": "Invalid filename format"}), 400

        audit_log("RUN_SCRIPT", f"filename={filename}")
        result = script_manager.run_script(filename)
        return jsonify({"success": True, "data": result})
    except FileNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error running script: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/scripts/running', methods=['GET'])
@rate_limit
@require_api_key
def get_running_scripts():
    """Get all currently running scripts"""
    try:
        scripts = script_manager.get_running_scripts()
        return jsonify({"success": True, "data": scripts})
    except Exception as e:
        logger.error(f"Error getting running scripts: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/scripts/status/<run_id>', methods=['GET'])
@rate_limit
@require_api_key
def get_script_status(run_id):
    """Get status of a script execution"""
    try:
        if not validate_input(run_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid run ID format"}), 400

        status = script_manager.get_script_status(run_id)
        return jsonify({"success": True, "data": status})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error getting script status: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/scripts/stop/<run_id>', methods=['POST'])
@rate_limit
@require_api_key
def stop_script(run_id):
    """Stop a running script"""
    try:
        if not validate_input(run_id, 'uuid'):
            return jsonify({"success": False, "error": "Invalid run ID format"}), 400

        audit_log("STOP_SCRIPT", f"run_id={run_id}")
        result = script_manager.stop_script(run_id)
        return jsonify({"success": True, "data": result})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        logger.error(f"Error stopping script: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


# ============== DOCKER API ==============

@app.route('/api/docker/status', methods=['GET'])
@rate_limit
@require_api_key
def docker_status():
    """Check if Docker is available"""
    try:
        available = docker_manager.is_docker_available()
        return jsonify({"success": True, "data": {"available": available}})
    except Exception as e:
        return jsonify({"success": True, "data": {"available": False}})


@app.route('/api/docker/containers', methods=['GET'])
@rate_limit
@require_api_key
def list_containers():
    """List all Docker containers"""
    try:
        all_containers = request.args.get('all', 'true').lower() == 'true'
        containers = docker_manager.list_containers(all_containers)
        return jsonify({"success": True, "data": containers})
    except Exception as e:
        logger.error(f"Error listing containers: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/docker/containers/<container_id>/start', methods=['POST'])
@rate_limit
@require_api_key
def start_container(container_id):
    """Start a Docker container"""
    try:
        if not validate_input(container_id, 'container_id', max_length=128):
            return jsonify({"success": False, "error": "Invalid container ID format"}), 400

        audit_log("START_CONTAINER", f"container_id={container_id}")
        result = docker_manager.start_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error starting container: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/docker/containers/<container_id>/stop', methods=['POST'])
@rate_limit
@require_api_key
def stop_container(container_id):
    """Stop a Docker container"""
    try:
        if not validate_input(container_id, 'container_id', max_length=128):
            return jsonify({"success": False, "error": "Invalid container ID format"}), 400

        audit_log("STOP_CONTAINER", f"container_id={container_id}")
        result = docker_manager.stop_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error stopping container: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/docker/containers/<container_id>/restart', methods=['POST'])
@rate_limit
@require_api_key
def restart_container(container_id):
    """Restart a Docker container"""
    try:
        if not validate_input(container_id, 'container_id', max_length=128):
            return jsonify({"success": False, "error": "Invalid container ID format"}), 400

        audit_log("RESTART_CONTAINER", f"container_id={container_id}")
        result = docker_manager.restart_container(container_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error restarting container: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route('/api/docker/containers/<container_id>/logs', methods=['GET'])
@rate_limit
@require_api_key
def get_container_logs(container_id):
    """Get container logs"""
    try:
        if not validate_input(container_id, 'container_id', max_length=128):
            return jsonify({"success": False, "error": "Invalid container ID format"}), 400

        # Validate and limit tail parameter
        try:
            tail = min(max(int(request.args.get('tail', 100)), 1), 10000)
        except (ValueError, TypeError):
            tail = 100

        result = docker_manager.get_container_logs(container_id, tail)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error getting container logs: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


# WebSocket Events

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected from {request.remote_addr}")
    emit('connected', {'message': 'Connected to automation server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected from {request.remote_addr}")


@socketio.on('request_status')
def handle_status_request(data):
    """Handle status request"""
    try:
        data = data or {}
        automation_id = sanitize_string(data.get('automation_id', ''))

        if automation_id:
            if not validate_input(automation_id, 'uuid'):
                emit('error', {'message': 'Invalid automation ID format'})
                return
            status = manager.get_status(automation_id)
            emit('status_update', status)
        else:
            statuses = manager.list_automations()
            emit('status_update', statuses)
    except ValueError as e:
        emit('error', {'message': str(e)})
    except Exception:
        emit('error', {'message': 'Internal server error'})


# Health check endpoint (no auth required)
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    logger.info("Starting Automation Server...")
    logger.info(f"HTTPS Enabled: {Config.HTTPS_ENABLED}")
    logger.info(f"API Key Required: {Config.API_KEY_REQUIRED}")
    logger.info(f"Rate Limiting: {Config.RATE_LIMIT_ENABLED}")

    ssl_context = None
    if Config.HTTPS_ENABLED:
        ssl_context = (Config.SSL_CERT, Config.SSL_KEY)
        logger.info(f"Using SSL certificate: {Config.SSL_CERT}")

    # In production (DEBUG=False), allow werkzeug for simplicity
    # For high-traffic production, use: gunicorn --worker-class eventlet -w 1 app:app
    socketio.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        allow_unsafe_werkzeug=True,  # Safe behind reverse proxy (nginx)
        ssl_context=ssl_context
    )

