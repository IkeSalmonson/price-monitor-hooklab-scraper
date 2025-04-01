# Price Monitor 
Solução para o desafio técnico de Desenvolvedor Python Pleno (Foco em Dados) da Hooklab. Implementa web scraping de Amazon e Magazine Luiza com Celery para processamento assíncrono. (Opcional 1) Containerizado com Docker. (Opcional 2 ) API em Flask ou FastAPI para consulta de preços recentes.

## Como usar

 Para iniciar a aplicação é necessário ter: 
    - Docker    
    - Docker Compose

 Para construir as imagens e iniciar os serviços:
```
docker compose up --build  
```
O monitor (Celery Flower) esta direcionado Celery Flower http://localhost:5557 <br>

As requisições para extração de informação do produto são no formato: <br>
    http://localhost:8010/scrape?url={url} <br>
    Exemplos no arquivo: ./src/scrapper/dev_examples/requests.rest
#### Send URL to scrape Magalu 
GET http://localhost:8010/scrape?url=https://www.magazineluiza.com.br/jornada-api-na-pratica-brasport/p/hkbbj6e62g/li/otli/

#### Send URL to scrape Amazon
GET http://localhost:8010/scrape?url=https://www.amazon.com.br/Jornada-pr%C3%A1tica-Alessandro-Antonio-Brito/dp/658843197X/

#### Considerações 
    A versão atual da aplicação depende de html salvos localmente nos exemplos de desenvolvimento. 
    Ambos marketplaces colocam impedimentos a requests de sistemas automatizados e informam que é necessário utilizar meios aprovados por seus acordos de uso da plataforma.
    
 


