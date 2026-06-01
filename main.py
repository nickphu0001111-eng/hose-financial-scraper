#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Công cụ scrape dữ liệu tài chính từ VietStock
Thu thập: Asset, Doanh thu, LNST, VCSH của tất cả cổ phiếu HOSE (2020-2025)
"""

import logging
import sys
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
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║   🏢 HOSE Financial Data Scraper - VietStock                              ║
    ║   📊 Thu thập: Asset, Doanh thu, LNST, VCSH                               ║
    ║   📅 Giai đoạn: 2020-2025 | Tất cả cổ phiếu HOSE                         ║
    ║   🔗 Nguồn: VietStock API                                                 ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Khởi động...")
    
    try:
        # Bước 1: Lấy danh sách cổ phiếu HOSE
        stocks = HOSEStockList.get_all_stocks()
        
        if not stocks or len(stocks) == 0:
            logger.error("\n❌ KHÔNG THỂ TIẾP TỤC: Không lấy được danh sách cổ phiếu")
            return 1
        
        logger.info(f"\n✅ Lấy được {len(stocks)} cổ phiếu HOSE")
        
        # Bước 2: Khởi tạo scraper
        logger.info("\n" + "="*60)
        logger.info("Bước 2: Khởi tạo Scraper")
        logger.info("="*60)
        scraper = VietStockScraper()
        logger.info("✅ Scraper đã sẵn sàng")
        
        # Bước 3: Scrape dữ liệu
        logger.info("\n" + "="*60)
        logger.info("Bước 3: Bắt đầu Scrape Dữ Liệu")
        logger.info("="*60)
        logger.info(f"\n⏳ Điều này có thể mất vài giờ:")
        logger.info(f"   - Số cổ phiếu: {len(stocks):,}")
        logger.info(f"   - Số năm: 6 (2020-2025)")
        logger.info(f"   - Tổng requests: {len(stocks) * 6:,}")
        logger.info(f"   - Với delay 1-2 giây/request, ước tính: ~{len(stocks) * 6 / 60:.0f} phút\n")
        
        scraper.scrape_all_stocks(stocks, years=range(2020, 2026))
        
        # Bước 4: Lưu dữ liệu
        logger.info("\n" + "="*60)
        logger.info("Bước 4: Lưu Dữ Liệu")
        logger.info("="*60)
        scraper.save_to_file('both')
        
        # Bước 5: Hiển thị kết quả
        logger.info("\n" + "="*60)
        logger.info("Bước 5: Kết Quả")
        logger.info("="*60)
        df = scraper.get_dataframe()
        
        if len(df) > 0:
            print("\n" + "="*80)
            print("✅ HỌ̀AN THÀǸH!")
            print("="*80)
            print(f"\n📊 Thống Kê:")
            print(f"   - Tổng records: {len(df):,}")
            print(f"   - Cổ phiếu duy nhất: {df['code'].nunique():,}")
            print(f"   - Năm: {df['year'].min()}-{df['year'].max()}")
            print(f"   - Ngành: {df['industry'].nunique()} ngành")
            print(f"\n💰 Thống Kê Tài Chính (VND):")
            print(f"   - Asset trung bình: {df['asset'].mean():,.0f}")
            print(f"   - Doanh thu trung bình: {df['revenue'].mean():,.0f}")
            print(f"   - LNST trung bình: {df['lnst'].mean():,.0f}")
            print(f"   - VCSH trung bình: {df['vcsh'].mean():,.0f}")
            
            print(f"\n📁 File output: output/hose_financial_data_*.csv/.xlsx")
            print(f"\n🏆 Top 10 công ty theo Asset:")
            top_assets = df.groupby('code')[['asset', 'name']].first().sort_values('asset', ascending=False).head(10)
            for idx, (code, row) in enumerate(top_assets.iterrows(), 1):
                print(f"   {idx:2d}. {code:6s} - {row['name']:40s} - {row['asset']:>15,.0f} VND")
            
            print(f"\n📋 Top 10 công ty theo Doanh Thu:")
            top_revenue = df.groupby('code')[['revenue', 'name']].first().sort_values('revenue', ascending=False).head(10)
            for idx, (code, row) in enumerate(top_revenue.iterrows(), 1):
                print(f"   {idx:2d}. {code:6s} - {row['name']:40s} - {row['revenue']:>15,.0f} VND")
            
            print(f"\n✅ Scraping hoàn tất thành công!")
            print("="*80)
        else:
            logger.error("❌ Không có dữ liệu được lấy!")
            return 1
        
        return 0
    
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Người dùng dừng chương trình")
        return 1
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
