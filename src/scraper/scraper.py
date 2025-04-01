# src/scraper/scraper.py
""" Modulo com a função para definir e executar scraper de acordo com o input na aplicação"""
from abc import ABC, abstractmethod
import re
from .magalu_scraper import MagaluProductScraper
from .amazon_scraper import AmazonProductScraper


class ProductScraper(ABC):
    """ Classe abstrata para definir e executar scraper de acordo com o input na aplicação"""

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

