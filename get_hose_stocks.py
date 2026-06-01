import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class HOSEStockList:
    """Lấy danh sách tất cả cổ phiếu HOSE từ VietStock API"""
    
    @staticmethod
    def get_from_vietstock():
        """
        Lấy danh sách cổ phiếu từ VietStock API - nguồn dữ liệu chính thức
        Sắp xếp theo A-Z
        """
        try:
            logging.info("🔍 Đang kết nối VietStock API...")
            url = "https://vietstock.vn/api/Stock/GetListByExchange"
            params = {'exchange': 'HOSE'}
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data'] and len(data['data']) > 0:
                # Trích xuất mã cổ phiếu
                stocks = [item['code'] for item in data['data']]
                # Sắp xếp A-Z
                stocks.sort()
                
                logging.info(f"✅ Lấy được {len(stocks)} cổ phiếu HOSE từ API (VietStock)")
                logging.info(f"   Phạm vi: {stocks[0]} - {stocks[-1]}")
                return stocks
            
            logging.warning("⚠️ API không trả về dữ liệu")
            return None
        
        except requests.exceptions.Timeout:
            logging.error("❌ Timeout khi kết nối VietStock API")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Lỗi kết nối API: {str(e)[:100]}")
            return None
        except Exception as e:
            logging.error(f"❌ Lỗi xử lý dữ liệu: {str(e)[:100]}")
            return None
    
    @staticmethod
    def get_from_alternative_source():
        """
        Lấy danh sách từ nguồn thay thế (nếu VietStock fail)
        """
        try:
            logging.info("🔄 Thử nguồn dữ liệu thay thế...")
            # Thử lấy từ endpoint khác của VietStock
            url = "https://vietstock.vn/api/Company/GetListByExchange"
            params = {'exchange': 'HOSE'}
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                stocks = [item.get('code') or item.get('symbol') for item in data['data']]
                stocks = [s for s in stocks if s]  # Lọc None values
                stocks.sort()
                
                if stocks:
                    logging.info(f"✅ Lấy được {len(stocks)} cổ phiếu từ nguồn thay thế")
                    return stocks
            
            return None
        
        except Exception as e:
            logging.warning(f"⚠️ Không lấy được từ nguồn thay thế: {str(e)[:50]}")
            return None
    
    @staticmethod
    def get_all_stocks():
        """
        Lấy toàn bộ danh sách cổ phiếu HOSE (ưu tiên từ API)
        Nếu API fail, trả về None và yêu cầu người dùng thử lại
        """
        logging.info("\n" + "="*60)
        logging.info("Bước 1: Lấy danh sách cổ phiếu HOSE")
        logging.info("="*60)
        
        # Cố gắng lấy từ VietStock API
        stocks = HOSEStockList.get_from_vietstock()
        
        if stocks:
            return stocks
        
        # Thử lấy từ nguồn thay thế
        stocks = HOSEStockList.get_from_alternative_source()
        
        if stocks:
            return stocks
        
        # Nếu cả hai đều fail
        logging.error("\n❌ KHÔNG THỂ LẤY DANH SÁCH CỔ PHIẾU!")
        logging.error("   - VietStock API không khả dụng")
        logging.error("   - Vui lòng kiểm tra:")
        logging.error("     1. Kết nối internet")
        logging.error("     2. VietStock.vn có còn hoạt động không")
        logging.error("     3. Thử chạy lại sau vài phút")
        return None
    
    @staticmethod
    def get_count(stocks):
        """Trả về số lượng cổ phiếu"""
        return len(stocks) if stocks else 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # Test
    stocks = HOSEStockList.get_all_stocks()
    if stocks:
        print(f"\n📊 Tổng cổ phiếu HOSE: {len(stocks)}")
        print(f"\n🎯 Top 20 cổ phiếu (A-Z):")
        for i, stock in enumerate(stocks[:20], 1):
            print(f"   {i:2d}. {stock}")
    else:
        print("\n⚠️ Không thể lấy danh sách cổ phiếu")
