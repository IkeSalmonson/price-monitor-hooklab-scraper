# src/scraper/magalu_scraper.py
from bs4 import BeautifulSoup
 
import logging
logger = logging.getLogger(__name__)

class MagaluProductScraper( ):
    def scrape_product(self, html_content: str) -> dict:
        """
        Extrai os dados do produto da página do Magazine Luiza.
        """
        logger.info("Iniciando scraping do Magazine Luiza")
        soup = BeautifulSoup(html_content, 'html.parser')
        product_data = {}

        # Nome do produto
        name_element = soup.find(  'h1', {'data-testid': 'heading-product-title'})
        product_data['name'] = name_element.text.strip() if name_element else None
        if product_data['name']:
            logger.info(f"Nome do produto encontrado: {product_data['name']}")
        else:
            logger.warning("Nome do produto não encontrado")

        # Preço à vista
        price_avista_element = soup.find('p', {'data-testid': 'price-value' })
        product_data['price_avista'] = price_avista_element.text.strip().replace('ou  ', '').replace('R$', '').replace('\xa0', '').replace(',', '.') if price_avista_element else None
        if product_data['price_avista']:
            logger.info(f"Preço à vista encontrado: {product_data['price_avista']}")
        else:
            logger.warning("Preço à vista não encontrado")

        # Preço a prazo (pode variar bastante na estrutura)
        price_parcelado_element = soup.find('div', {'data-testid':"creditCard-panel"}) # Tentativa inicial, pode precisar ajuste
        if price_parcelado_element  :
            product_data['price_a_prazo'] = self.parse_tabela_parcelado(price_parcelado_element)
            logger.info(f"Preço a prazo encontrado (via 'até'): {product_data['price_a_prazo']}")
        else:
            logger.warning("Preço a prazo não encontrado")

        # Disponibilidade (Verifica se há um elemento indicando indisponibilidade)
        availability_element = soup.find('p', class_='product-unavailable__title')
        product_data['disponibilidade'] = not bool(availability_element)
        logger.info(f"Disponibilidade: {'Em estoque' if product_data['disponibilidade'] else 'Indisponível'}")
        return product_data


    def parse_tabela_parcelado(self, credit_card_panel_soup):
        """
        Parser para extrair informações da tabela de parcelamento do cartão de crédito.
        """
        installments_data = []
        table = credit_card_panel_soup.find('table', {'data-testid': 'creditCard-table'})
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        installment_text = cells[0].find('span').text.strip()
                        installment_parts = installment_text.split('x de')
                        if len(installment_parts) == 2:
                            num_installments = installment_parts[0].strip()
                            installment_value = installment_parts[1].strip().replace('R$', '').replace('\xa0', '').replace(',', '.')
                        elif len(installment_parts) == 1: # For the first row
                            num_installments = "01" # Assuming 1x for the initial value
                            installment_value = installment_parts[0].strip().replace('R$', '').replace('\xa0', '').replace(',', '.')
                        interest_info = cells[0].find('p').text.strip()
                        total_value = cells[1].text.strip()
                        installments_data.append({
                            "installment_number": num_installments,
                            "installment_value": installment_value,
                            "interest_free": "sem juros" in interest_info,
                            "total_value": total_value.replace('R$', '').replace('\xa0', '').replace(',', '.') if total_value else installment_value.replace("R$&nbsp;", "")  
                        })
        return installments_data