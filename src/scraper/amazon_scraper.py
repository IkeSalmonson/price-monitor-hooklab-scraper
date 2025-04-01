# src/scraper/amazon_scraper.py
from bs4 import BeautifulSoup
 
import logging
logger = logging.getLogger(__name__)

class AmazonProductScraper( ):
    def scrape_product(self, html_content: str) -> dict:
        """
        Extrai os dados do produto da página da Amazon.
        Você precisará inspecionar o HTML da página para encontrar os seletores corretos.
        """
        logger.info("Iniciando scraping da Amazon")
 

        soup = BeautifulSoup(html_content, 'html.parser')
        product_data = {}

        # Nome do produto
        name_element = soup.find('span', id='productTitle') 
        product_data['name'] = name_element.text.strip() if name_element else None
        if product_data['name']:
            logger.info(f"Nome do produto encontrado: {product_data['name']}")
        else:
            logger.warning("Nome do produto não encontrado")

        # Preço à vista (geralmente em um elemento com alguma classe específica)
        price_avista_element = soup.find('span', class_='a-price-whole') # Este é um seletor comum, pode precisar ajuste
        if price_avista_element:
            price_text = price_avista_element.text.strip().replace('R$', '').replace('\xa0', '').replace(',', '.')
            # Tenta converter para float para verificar se é um preço válido
            try:
                product_data['price_avista'] = float(price_text)
                logger.info(f"Preço à vista encontrado: {product_data['price_avista']}")
            except ValueError:
                product_data['price_avista'] = price_text
                logger.warning(f"Preço à vista não encontrado ou em formato inválido: {price_text}")
        else:
            logger.warning("Preço à vista não encontrado")
            product_data['price_avista'] = None

        # Preço a prazo (pode estar em diferentes lugares dependendo da oferta)
        price_parcelado_element = soup.find('span', class_='a-size-base a-color-secondary') # Seção de parcelamento
        if price_parcelado_element and "em até" in price_parcelado_element.text.lower():
            product_data['price_a_prazo'] = price_parcelado_element.text.strip()
            logger.info(f"Preço a prazo encontrado: {product_data['price_a_prazo']}")
        else:
            product_data['price_a_prazo'] = None
            logger.warning("Preço a prazo não encontrado")

        # Disponibilidade (Verifica elementos como "Em estoque" ou "Indisponível")
        availability_element = soup.find('div', id='availability')
        if availability_element:
            availability_text = availability_element.get_text(strip=True).lower()
            product_data['disponibilidade'] = "em estoque" in availability_text
            logger.info(f"Disponibilidade: {'Em estoque' if product_data['disponibilidade'] else 'Indisponível'}")
        else:
            product_data['disponibilidade'] = False # Assume indisponível se não encontrar o elemento
            logger.warning("Informação de disponibilidade não encontrada")

        return product_data
