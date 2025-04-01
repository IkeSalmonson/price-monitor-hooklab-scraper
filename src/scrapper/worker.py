# src/worker.py
from celery import shared_task
from .scrapper import ProductScraper
import os
import requests
import json
from datetime import datetime
import logging.config
 
from hashlib import sha256

# Certifique-se de que a pasta de logs exista
log_dir = './data/log'
os.makedirs(log_dir, exist_ok=True)

# Carrega a configuração do logging a partir do arquivo .ini
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
# Obtém o logger específico para o módulo atual
logger = logging.getLogger(__name__)


@shared_task(name='tasks.divide')
def divide(x, y):
    import time
    time.sleep(5)
    logger.debug(f"divide(x, y): {x},{y}")
    return x / y

@shared_task(name='tasks.scrape_product')
def scrape_product(url):
    """
    Tarefa Celery para realizar o scraping de um produto em um dado URL.
    """
    logger.info(f"Iniciando tarefa de scraping para a URL: {url}")
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
        if re.search(r'magazineluiza\.com\.br', url):
            example_num = 1
        elif re.search(r'amazon\.com\.br', url):
            example_num = 2
 
        with open(f'./scrapper/dev_examples/exampleHTML{example_num}.html', 'r', encoding='utf-8') as arquivo:
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
            logger.warning(f"Nenhum scrapper disponível para o domínio da URL: {url}")
            return {"error": f"Nenhum scrapper disponível para o domínio da URL: {url}"}

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
    # hash url as sha256 13 character long filename
    hash = sha256(url.encode()).hexdigest()[:char_limit]
    filename = f"./data/product_{data['timestamp'].replace(':', '')}{hash}.json" # Caminho relativo dentro do container
    os.makedirs("./data", exist_ok=True)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            # set url attribute
            os.setxattr(filename, 'user.url', url.encode())
        logger.info(f"Dados salvos em: {filename}, url associado: {os.getxattr(filename, 'user.url').decode()}")
        return "Dados salvos com sucesso"
    except Exception as e:
        logger.error(f"Erro ao salvar os dados em {filename}: {e}", exc_info=True)
        return f"Erro ao salvar os dados: {e}"

if __name__ == '__main__':
    # Exemplo de como rodar o worker localmente (para testes)
    # celery -A worker worker -l info
    pass