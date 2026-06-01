#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Công cụ scrape dữ liệu tài chính từ VietStock
Thu thập: Asset, Doanh thu, LNST, VCSH của 566 công ty HOSE (2020-2025)
"""

import logging
from scraper import VietStockScraper
from get_hose_stocks import HOSEStockList

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    print("""
    ╔════════════════════════════════════════════════════╗
    ║   HOSE Financial Data Scraper - VietStock         ║
    ║   Thu thập: Asset, Doanh thu, LNST, VCSH          ║
    ║   Giai đoạn: 2020-2025 | 566 công ty HOSE        ║
    ╚════════════════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Khởi động...")
    
    # Bước 1: Lấy danh sách cổ phiếu HOSE
    logger.info("📋 Bước 1: Lấy danh sách cổ phiếu HOSE...")
    stocks = HOSEStockList.get_from_vietstock()
    
    if not stocks:
        logger.warning("⚠️ Không lấy được danh sách từ API, dùng danh sách hardcode...")
        stocks = HOSEStockList.get_hardcoded()
    
    logger.info(f"📊 Tổng cổ phiếu: {len(stocks)}")
    
    # Bước 2: Scrape dữ liệu
    logger.info("🔄 Bước 2: Bắt đầu scrape dữ liệu...")
    scraper = VietStockScraper()
    scraper.scrape_all_stocks(stocks, years=range(2020, 2026))
    
    # Bước 3: Lưu dữ liệu
    logger.info("💾 Bước 3: Lưu dữ liệu...")
    scraper.save_to_file('both')
    
    # Bước 4: Hiển thị kết quả
    logger.info("📈 Bước 4: Kết quả...")
    df = scraper.get_dataframe()
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH!")
    print("="*60)
    print(f"\n📊 Thống kê:")
    print(f"   - Tổng records: {len(df)}")
    print(f"   - Cổ phiếu duy nhất: {df['code'].nunique()}")
    print(f"   - Năm: {df['year'].min()}-{df['year'].max()}")
    print(f"\n📁 File output: output/hose_financial_data_*.csv/.xlsx")
    print(f"\n📄 Top 10 records:")
    print(df.head(10).to_string(index=False))

if __name__ == '__main__':
    main()
