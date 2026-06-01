# 🏦 HOSE Financial Data Scraper

**Công cụ scrape dữ liệu tài chính từ VietStock**

## 📊 Thông tin dự án

- **Mục đích**: Thu thập dữ liệu tài chính của 566 công ty trên sàn HOSE
- **Chỉ số**: Asset, Doanh thu, LNST (Lợi nhuận ròng), VCSH (Vốn chủ sở hữu)
- **Giai đoạn**: 2020-2025
- **Nguồn dữ liệu**: VietStock (https://vietstock.vn)

## 🛠️ Cài đặt

### Yêu cầu
- Python 3.8+
- pip
- Chrome browser (cho Selenium scraper)

### Bước 1: Clone repository
```bash
git clone https://github.com/nickphu0001111-eng/hose-financial-scraper.git
cd hose-financial-scraper
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

**LƯU Ý**: Selenium sẽ tự động tải ChromeDriver via `webdriver-manager`. Không cần tải thủ công!

## 📝 Cách sử dụng

### Chạy scraper API (cũ)
```bash
python scraper.py
```

### Chạy Selenium scraper (mới - khuyến nghị) ⭐
```bash
python scraper_selenium.py
```

**Ưu điểm Selenium**:
- ✅ Tự động tải ChromeDriver (không cần download)
- ✅ Mở browser thật → VietStock không chặn
- ✅ Có thể lấy dữ liệu JavaScript
- ✅ Không phụ thuộc vào API VietStock
- ✅ Dễ cập nhật khi VietStock thay đổi layout

### Output
Dữ liệu sẽ được lưu vào folder `output/`:
- `hose_financial_data_YYYYMMDD_HHMMSS.csv`
- `hose_financial_data_YYYYMMDD_HHMMSS.xlsx`

## 📋 Cấu trúc dữ liệu

| Cột | Mô tả | Kiểu dữ liệu |
|-----|-------|---------------|
| code | Mã cổ phiếu | string |
| name | Tên công ty | string |
| industry | Ngành công nghiệp | string |
| price | Giá cổ phiếu | string |
| market_cap | Vốn hóa thị trường | string |
| pe_ratio | Chỉ số P/E | string |

## 🔧 Tuỳ chỉnh

### Thay đổi danh sách cổ phiếu
Sửa file `scraper_selenium.py`:
```python
sample_stocks = [
    'VCB', 'VIC', 'BID', 'CTG', 'VNM', 'FPT', 'MWG', 'PNJ', 'TCB', 'ACB'
]
```

Thêm mã cổ phiếu khác theo nhu cầu.

### Thay đổi output format
```python
scraper.save_to_file('csv')    # Chỉ CSV
scraper.save_to_file('excel')  # Chỉ Excel
scraper.save_to_file('both')   # Cả hai (default)
```

## 📊 Ví dụ output

```
code    name                           industry        price       market_cap          pe_ratio
----    ----                           --------        -----       ----------          --------
VCB     Ngân hàng Thương mại Cổ phần   Banking         82,100      250,500,000,000     8.5
VIC     Tập đoàn Masan                 Diversified     55,900      180,200,000,000     12.3
BID     Ngân hàng TMCP Ngân hàng Đầu   Banking         28,650      120,000,000,000     6.2
```

## ⚠️ Lưu ý quan trọng

### Selenium
- ✅ **Tự động tải ChromeDriver** via `webdriver-manager`
- 🔧 Đảm bảo bạn đã cài Chrome browser
- ⏱️ Mỗi cổ phiếu mất ~5 giây (do phải mở browser)
- 🚫 VietStock có thể block nếu request quá nhanh (scraper đã có delay 2 giây)

### Log files
- `scraper.log` - Log từ API scraper (cũ)
- `scraper_selenium.log` - Log từ Selenium scraper (mới)

## 🐛 Troubleshooting

### Lỗi: "ChromeDriver not found"
**Giải pháp**: Cài đặt lại `webdriver-manager`
```bash
pip install --upgrade webdriver-manager
```

### Lỗi: "Chrome not found"
**Giải pháp**: Cài đặt Chrome browser hoặc sửa path trong code
```python
# Nếu dùng Firefox thay vì Chrome
from selenium.webdriver import Firefox
driver = Firefox(service=Service(GeckoDriverManager().install()))
```

### Lỗi: "Connection timeout"
**Giải pháp**: Kiểm tra kết nối internet hoặc tăng timeout
```python
time.sleep(5)  # Tăng từ 3 -> 5 giây
```

### Lỗi: "Element not found"
**Nguyên nhân**: VietStock đã thay đổi HTML structure  
**Giải pháp**: Cập nhật CSS selectors trong hàm `_extract_*`

## 📈 Cải tiến tương lai

- [ ] Hỗ trợ scrape từ các nguồn khác (SSI, TCBS, CafeF)
- [ ] Xây dựng database SQLite/PostgreSQL
- [ ] Dashboard Plotly/Streamlit để visualize
- [ ] Scheduling tự động update dữ liệu hàng tháng (APScheduler)
- [ ] REST API để query dữ liệu
- [ ] Cải thiện HTML parser (thêm chỉ số tài chính)
- [ ] Hỗ trợ multi-threading/async scraping
- [ ] Unit tests và integration tests

## 📞 Hỗ trợ & Báo cáo lỗi

Nếu gặp vấn đề:
1. ✅ Kiểm tra log file (`scraper.log` hoặc `scraper_selenium.log`)
2. ✅ Mở **GitHub Issue** với mô tả lỗi chi tiết
3. ✅ Kiểm tra **Troubleshooting** section trên

## 📄 License

MIT License - Tự do sử dụng cho mục đích không lợi nhuận

---

**Last Updated**: 2026-06-01  
**Author**: @nickphu0001111-eng  
**Status**: ✅ Active Development
