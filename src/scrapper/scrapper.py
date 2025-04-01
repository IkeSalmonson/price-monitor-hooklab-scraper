# src/scrapper.py
from abc import ABC, abstractmethod
from .magalu_scrapper import MagaluProductScraper
from .amazon_scrapper import AmazonProductScraper
import re

class ProductScraper(ABC):
    @abstractmethod
    def scrape_product(self, html_content: str) -> dict:
        """
        Método para extrair os dados de um produto do conteúdo HTML.
        Deve ser implementado pelas subclasses específicas de cada site.
        """
        pass

    @staticmethod
    def get_scraper(url: str):
        """
        Método estático para determinar e retornar a instância do scrapper correto
        com base no domínio da URL.
        """

        if re.search(r'magazineluiza\.com\.br', url):
            return MagaluProductScraper()
        elif re.search(r'amazon\.com\.br', url):
            return AmazonProductScraper()
        else:
            return None

 