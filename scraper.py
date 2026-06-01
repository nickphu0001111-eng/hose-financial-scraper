import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import logging
from retrying import retry
import os

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VietStockScraper:
    def __init__(self):
        self.base_url = "https://vietstock.vn"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.data = []
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def fetch_stock_financials(self, stock_code, year):
        """
        Truy vấn dữ liệu tài chính từ VietStock
        """
        try:
            # URL API VietStock (có thể cần điều chỉnh)
            url = f"{self.base_url}/api/Finance/GetFinancialHighlightReport"
            
            params = {
                'code': stock_code,
                'year': year,
                'type': 'ANNUAL'  # ANNUAL hoặc QUARTERLY
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Lỗi khi truy vấn {stock_code} năm {year}: {e}")
            return None
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def fetch_stock_info(self, stock_code):
        """
        Lấy thông tin cơ bản của cổ phiếu
        """
        try:
            url = f"{self.base_url}/{stock_code}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse dữ liệu từ HTML
            info = {
                'code': stock_code,
                'name': self._extract_name(soup),
                'industry': self._extract_industry(soup)
            }
            
            return info
        
        except Exception as e:
            logger.error(f"Lỗi khi lấy thông tin {stock_code}: {e}")
            return None
    
    def _extract_name(self, soup):
        """Trích tên công ty"""
        try:
            name_elem = soup.find('h1', class_='company-name')
            return name_elem.text.strip() if name_elem else 'N/A'
        except:
            return 'N/A'
    
    def _extract_industry(self, soup):
        """Trích ngành công nghiệp"""
        try:
            industry_elem = soup.find('span', class_='industry')
            return industry_elem.text.strip() if industry_elem else 'N/A'
        except:
            return 'N/A'
    
    def scrape_all_stocks(self, stock_codes, years=range(2020, 2026)):
        """
        Scrape dữ liệu tất cả cổ phiếu
        """
        total_stocks = len(stock_codes)
        
        for idx, stock_code in enumerate(stock_codes, 1):
            logger.info(f"[{idx}/{total_stocks}] Đang xử lý: {stock_code}")
            
            # Lấy thông tin cơ bản
            stock_info = self.fetch_stock_info(stock_code)
            
            # Lấy dữ liệu tài chính từng năm
            for year in years:
                financials = self.fetch_stock_financials(stock_code, year)
                
                if financials and 'data' in financials:
                    record = {
                        'code': stock_code,
                        'name': stock_info.get('name', 'N/A') if stock_info else 'N/A',
                        'industry': stock_info.get('industry', 'N/A') if stock_info else 'N/A',
                        'year': year,
                        'asset': financials['data'].get('asset', 0),
                        'revenue': financials['data'].get('revenue', 0),
                        'lnst': financials['data'].get('netIncome', 0),  # Lợi nhuận ròng
                        'vcsh': financials['data'].get('equityTotal', 0),  # Vốn chủ sở hữu
                    }
                    self.data.append(record)
                
                # Delay để tránh bị block
                time.sleep(1)
            
            # Delay giữa các cổ phiếu
            time.sleep(2)
        
        logger.info(f"✅ Hoàn thành scrape. Tổng records: {len(self.data)}")
    
    def save_to_file(self, output_format='both'):
        """
        Lưu dữ liệu ra file
        output_format: 'csv', 'excel', hoặc 'both'
        """
        if not self.data:
            logger.warning("Không có dữ liệu để lưu!")
            return
        
        df = pd.DataFrame(self.data)
        
        # Tạo folder output nếu chưa có
        os.makedirs('output', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format in ['csv', 'both']:
            csv_file = f'output/hose_financial_data_{timestamp}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            logger.info(f"✅ Dữ liệu CSV: {csv_file}")
        
        if output_format in ['excel', 'both']:
            excel_file = f'output/hose_financial_data_{timestamp}.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')
            logger.info(f"✅ Dữ liệu Excel: {excel_file}")
    
    def get_dataframe(self):
        """Trả về DataFrame"""
        return pd.DataFrame(self.data)


if __name__ == '__main__':
    # Danh sách 566 cổ phiếu HOSE (cần lấy từ nguồn chính thức)
    # Để demo, dùng một số cổ phiếu phổ biến
    sample_stocks = [
        'VCB', 'VIC', 'BID', 'CTG', 'VNM', 'FPT', 'MWG', 'PNJ', 'TCB', 'ACB',
        'TPB', 'SBT', 'STB', 'HDB', 'MSN', 'SSI', 'VJC', 'VRE', 'PLX', 'DXG'
    ]
    
    logger.info("🚀 Bắt đầu scrape dữ liệu VietStock...")
    
    scraper = VietStockScraper()
    scraper.scrape_all_stocks(sample_stocks)
    scraper.save_to_file('both')
    
    # In kết quả
    df = scraper.get_dataframe()
    print("\n📊 Dữ liệu tài chính:")
    print(df.head(10))
    print(f"\nTổng records: {len(df)}")
