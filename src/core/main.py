#src/core/main.py
from core.app import create_app 
app = create_app()
celery = app.celery_app
 
 