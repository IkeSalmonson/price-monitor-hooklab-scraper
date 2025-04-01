# src/scraper/worker.py
"""Modulo com as funções relacionadas ao Scraping a serem executadas pelos Workers do Celery"""
import os
import json
from datetime import datetime
import logging.config
from hashlib import sha256
import requests
from celery import shared_task
from .scraper import ProductScraper

# Certifique-se de que a pasta de logs exista
LOGDIR = './data/log'
os.makedirs(LOGDIR, exist_ok=True)

# Carrega a configuração do logging a partir do arquivo .ini
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
# Obtém o logger específico para o módulo atual
logger = logging.getLogger(__name__)


@shared_task(name='tasks.divide')
def divide(x, y):
    """
    Tarefa Celery para testar se os containers workers conseguem executar função assincrona .
    """
    import time
    time.sleep(5)
    logger.debug(f"divide(x, y): {x},{y}")
    return x / y

@shared_task(name='tasks.scrape_product')
def scrape_product(url):
    """
    Tarefa Celery para realizar o scraping de um produto em um dado URL.
    """
    logger.info("Iniciando tarefa de scraping para a URL: %s",url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        ## Request necessitam de uma autorização para acessar o conteúdo dos URLs
        #response = requests.get(url, headers=headers)
        #response.raise_for_status()  # Raise an exception for bad status codes
        #html_content = response.text

        scraper = ProductScraper.get_scraper(url)

        ## Request Arquivo local
        import re
        example_num = 0
        if re.search(r'magazineluiza\.com\.br', url):
            example_num = 1
        elif re.search(r'amazon\.com\.br', url):
            example_num = 2

        with open(f'./scraper/dev_examples/exampleHTML{example_num}.html', 'r', encoding='utf-8') as arquivo:
            html_content = arquivo.read()

        if scraper:
            logger.info(f"Scraper encontrado: {scraper.__class__.__name__} para a URL: {url}")
            product_data = scraper.scrape_product(html_content)
            timestamp = datetime.now().isoformat()
            product_data['url'] = url
            product_data['timestamp'] = timestamp
            save_status = save_data(product_data)
            return {"message": f"Scraping bem-sucedido de {url}", "data": product_data, "save_status": save_status}
        else:
            logger.warning(f"Nenhum scraper disponível para o domínio da URL: {url}")
            return {"error": f"Nenhum scraper disponível para o domínio da URL: {url}"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar a URL {url}: {e}")
        return {"error": f"Erro ao acessar a URL {url}: {e}"}
    except Exception as e:
        logger.error(f"Ocorreu um erro durante o scraping da URL {url}: {e}", exc_info=True)
        return {"error": f"Ocorreu um erro durante o scraping da URL {url}: {e}" }

def save_data(data, char_limit=10):
    """
    Função para salvar os dados extraídos em um arquivo JSON.
    """
    logger.info(f"Salvando dados para o produto: {data.get('name')}")
    url = data['url']
    hash = sha256(url.encode()).hexdigest()[:char_limit]
    filename = f"./data/product_{data['timestamp'].replace(':', '')}{hash}.json"
    os.makedirs("./data", exist_ok=True)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            os.setxattr(filename, 'user.url', url.encode())
        logger.info(f"Dados salvos em: {filename}, url associado: {os.getxattr(filename, 'user.url').decode()}")
        return "Dados salvos com sucesso"
    except Exception as e:
        logger.error("Erro ao salvar os dados em %s: %s",filename,e, exc_info=True)
        return f"Erro ao salvar os dados: {e}"
