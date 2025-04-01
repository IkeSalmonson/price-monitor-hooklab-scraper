#src/core/main.py
"""Modulo para inicializar a aplicação e sua dependencia com celery"""
from core.app import create_app
app = create_app()
celery = app.celery_app 
 