import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class HOSEStockList:
    """Lấy danh sách tất cả cổ phiếu HOSE"""
    
    @staticmethod
    def get_from_vietstock():
        """
        Lấy danh sách cổ phiếu từ VietStock
        """
        try:
            url = "https://vietstock.vn/api/Stock/GetListByExchange"
            params = {'exchange': 'HOSE'}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                stocks = [item['code'] for item in data['data']]
                logging.info(f"✅ Lấy được {len(stocks)} cổ phiếu HOSE")
                return stocks
            
            return []
        
        except Exception as e:
            logging.error(f"Lỗi khi lấy danh sách: {e}")
            return []
    
    @staticmethod
    def get_hardcoded():
        """
        Danh sách cổ phiếu HOSE được hardcode (để dev)
        Cần update với danh sách đầy đủ 566 công ty
        """
        hose_stocks = [
            'VCB', 'VIC', 'BID', 'CTG', 'VNM', 'FPT', 'MWG', 'PNJ', 'TCB', 'ACB',
            'TPB', 'SBT', 'STB', 'HDB', 'MSN', 'SSI', 'VJC', 'VRE', 'PLX', 'DXG',
            'CEO', 'GMD', 'HDC', 'PVI', 'NT2', 'PPC', 'KBC', 'PVD', 'VCG', 'NKG',
        ]
        return hose_stocks


if __name__ == '__main__':
    # Test
    stocks = HOSEStockList.get_from_vietstock()
    print(f"Tổng cổ phiếu HOSE: {len(stocks)}")
    print(stocks[:10])
