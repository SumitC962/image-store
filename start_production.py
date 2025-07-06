#!/usr/bin/env python3
"""
Production startup script for Secure Image Storage
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from app import app

def setup_logging():
    """Setup production logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    
    # Setup app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('Secure Image Storage startup')

if __name__ == '__main__':
    setup_logging()
    
    # Production settings
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Run with Gunicorn-like settings
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        threaded=True
    ) 