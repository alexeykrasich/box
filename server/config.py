"""
Security Configuration - Production-Ready Settings
"""
import os
import secrets
import re
from functools import wraps
from flask import request, jsonify, g
from datetime import datetime
import logging

# Security logger
security_logger = logging.getLogger('security')


class Config:
    """Application configuration from environment variables"""
    
    # Secret key - MUST be set in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # API Authentication
    API_KEY = os.environ.get('API_KEY')
    API_KEY_REQUIRED = os.environ.get('API_KEY_REQUIRED', 'true').lower() == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60'))
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    
    # TLS/SSL
    SSL_CERT = os.environ.get('SSL_CERT')
    SSL_KEY = os.environ.get('SSL_KEY')
    HTTPS_ENABLED = bool(SSL_CERT and SSL_KEY)
    
    # Server
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'",
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Cache-Control': 'no-store, no-cache, must-revalidate',
        'Pragma': 'no-cache'
    }


# Input validation patterns
PATTERNS = {
    'uuid': re.compile(r'^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$|^[a-f0-9]{8}$'),
    'container_id': re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$'),
    'filename': re.compile(r'^[a-zA-Z0-9_.-]+\.(py|sh|bash)$'),
    'automation_type': re.compile(r'^[A-Za-z][A-Za-z0-9_]*$'),
}


def validate_input(value: str, pattern_name: str, max_length: int = 255) -> bool:
    """Validate input against predefined patterns"""
    if not value or not isinstance(value, str):
        return False
    if len(value) > max_length:
        return False
    pattern = PATTERNS.get(pattern_name)
    if pattern:
        return bool(pattern.match(value))
    return False


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input"""
    if not isinstance(value, str):
        return ''
    # Remove null bytes and control characters
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value[:max_length]


# Simple in-memory rate limiter
class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}  # ip -> list of timestamps
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is allowed"""
        now = datetime.now().timestamp()
        minute_ago = now - 60
        
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean old entries
        self.requests[client_ip] = [t for t in self.requests[client_ip] if t > minute_ago]
        
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return False
        
        self.requests[client_ip].append(now)
        return True


rate_limiter = RateLimiter(Config.RATE_LIMIT_PER_MINUTE)


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Config.API_KEY_REQUIRED:
            return f(*args, **kwargs)
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not Config.API_KEY:
            security_logger.warning("API_KEY not configured but API_KEY_REQUIRED is true")
            return jsonify({"success": False, "error": "Server misconfigured"}), 500
        
        if not api_key or not secrets.compare_digest(api_key, Config.API_KEY):
            security_logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({"success": False, "error": "Invalid or missing API key"}), 401
        
        return f(*args, **kwargs)
    return decorated


def rate_limit(f):
    """Decorator to apply rate limiting"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Config.RATE_LIMIT_ENABLED:
            return f(*args, **kwargs)
        
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        if not rate_limiter.is_allowed(client_ip):
            security_logger.warning(f"Rate limit exceeded for {client_ip}")
            return jsonify({"success": False, "error": "Rate limit exceeded"}), 429
        
        return f(*args, **kwargs)
    return decorated


def audit_log(action: str, details: str = ""):
    """Log security-relevant actions"""
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    security_logger.info(f"AUDIT: {action} | IP: {client_ip} | {details}")

