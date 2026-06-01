import time
import logging
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

# Cau hinh logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_selenium.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VietStockSeleniumScraper:
    def __init__(self):
        """Khoi tao Selenium WebDriver"""
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            self.data = []
            logger.info("✓ Khoi tao WebDriver thanh cong")
        except Exception as e:
            logger.error(f"Loi khoi tao WebDriver: {e}")
            raise

    def fetch_stock_financials(self, stock_code):
        """
        Lay du lieu tai chinh cua co phieu tu VietStock
        """
        try:
            url = f"https://vietstock.vn/chung-khoan/{stock_code.lower()}.htm"
            logger.info(f"Dang truy cap: {url}")
            
            self.driver.get(url)
            
            # Cho trang load
            time.sleep(3)
            
            # Parse HTML
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Tim du lieu tai chinh
            financial_data = self._extract_financial_data(soup, stock_code)
            
            return financial_data
        
        except Exception as e:
            logger.error(f"Loi khi lay du lieu {stock_code}: {e}")
            return None

    def _extract_financial_data(self, soup, stock_code):
        """
        Trich xuat du lieu tai chinh tu HTML
        """
        try:
            info = {
                'code': stock_code,
                'name': self._extract_name(soup),
                'industry': self._extract_industry(soup),
                'price': self._extract_price(soup),
                'market_cap': self._extract_market_cap(soup),
                'pe_ratio': self._extract_pe_ratio(soup),
            }
            return info
        except Exception as e:
            logger.error(f"Loi trich xuat du lieu: {e}")
            return None

    def _extract_name(self, soup):
        """Trich ten cong ty"""
        try:
            name_elem = soup.find('h1', class_='company-name')
            if name_elem:
                return name_elem.text.strip()
            return 'N/A'
        except:
            return 'N/A'

    def _extract_industry(self, soup):
        """Trich nganh cong nghiep"""
        try:
            industry_elem = soup.find('span', class_='industry')
            if industry_elem:
                return industry_elem.text.strip()
            return 'N/A'
        except:
            return 'N/A'

    def _extract_price(self, soup):
        """Trich gia co phieu"""
        try:
            price_elem = soup.find('span', class_='current-price')
            if price_elem:
                return price_elem.text.strip()
            return 'N/A'
        except:
            return 'N/A'

    def _extract_market_cap(self, soup):
        """Trich von hoa thi truong"""
        try:
            market_cap_elem = soup.find('span', class_='market-cap')
            if market_cap_elem:
                return market_cap_elem.text.strip()
            return 'N/A'
        except:
            return 'N/A'

    def _extract_pe_ratio(self, soup):
        """Trich chi so P/E"""
        try:
            pe_elem = soup.find('span', class_='pe-ratio')
            if pe_elem:
                return pe_elem.text.strip()
            return 'N/A'
        except:
            return 'N/A'

    def scrape_all_stocks(self, stock_codes):
        """
        Scrape du lieu tat ca co phieu
        """
        total_stocks = len(stock_codes)
        
        for idx, stock_code in enumerate(stock_codes, 1):
            logger.info(f"[{idx}/{total_stocks}] Dang xu ly: {stock_code}")
            
            # Lay du lieu
            financials = self.fetch_stock_financials(stock_code)
            
            if financials:
                self.data.append(financials)
            
            # Delay de tranh bi block
            time.sleep(2)
        
        logger.info(f"✓ Hoan thanh scrape. Tong records: {len(self.data)}")

    def save_to_file(self, output_format='both'):
        """
        Luu du lieu ra file
        output_format: 'csv', 'excel', hoac 'both'
        """
        if not self.data:
            logger.warning("Khong co du lieu de luu!")
            return
        
        df = pd.DataFrame(self.data)
        
        # Tao folder output neu chua co
        os.makedirs('output', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format in ['csv', 'both']:
            csv_file = f'output/hose_financial_data_{timestamp}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            logger.info(f"✓ Du lieu CSV: {csv_file}")
        
        if output_format in ['excel', 'both']:
            excel_file = f'output/hose_financial_data_{timestamp}.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')
            logger.info(f"✓ Du lieu Excel: {excel_file}")

    def get_dataframe(self):
        """Tra ve DataFrame"""
        return pd.DataFrame(self.data)

    def close(self):
        """Dong WebDriver"""
        self.driver.quit()
        logger.info("✓ Dong WebDriver")


if __name__ == '__main__':
    # Danh sach co phieu HOSE
    sample_stocks = [
        'VCB', 'VIC', 'BID', 'CTG', 'VNM', 'FPT', 'MWG', 'PNJ', 'TCB', 'ACB'
    ]
    
    logger.info("✓ Bat dau scrape du lieu VietStock bang Selenium...")
    
    scraper = VietStockSeleniumScraper()
    
    try:
        scraper.scrape_all_stocks(sample_stocks)
        scraper.save_to_file('both')
        
        # In ket qua
        df = scraper.get_dataframe()
        print("\n========== DU LIEU TAI CHINH ==========")
        print(df.head(10))
        print(f"\nTong records: {len(df)}")
    
    finally:
        scraper.close()
