#src/core/app.py
from fastapi import FastAPI, Query 
from utils.celery_utils import create_celery  
from scraper.worker import divide, scrape_product
import celery.states as states


def create_app() -> FastAPI:
    app = FastAPI()
    app.celery_app = create_celery()              
 
    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    
    @app.get("/divide/{param1}/{param2}")
    async def exec_divide(param1: int, param2: int)->str:
        task = app.celery_app.send_task('tasks.divide',  args=[param1, param2], kwargs={})
        response = f"<a href='{app.url_path_for('check_task', task_id=task.id)}'>check status of {task.id} </a>"
        return response

    @app.get("/check/{task_id}" )
    async def check_task(task_id: str) -> str:
        res = app.celery_app.AsyncResult(task_id)
        if res.state == states.PENDING:
            return res.state
        else:
            return str(res.result)
        
    @app.get("/scrape" )
    async def exec_scrape(url: str = Query(..., description="URL a ser analisada")) -> str:
        task = app.celery_app.send_task('tasks.scrape_product',   args=[url], kwargs={})
        response = f"<a href='{app.url_path_for('check_task', task_id=task.id)}'>check status de {task.id} </a>"
        return response
    
    return app