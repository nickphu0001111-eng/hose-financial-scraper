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

### Bước 1: Clone repository
```bash
git clone https://github.com/nickphu0001111-eng/hose-financial-scraper.git
cd hose-financial-scraper
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 📝 Cách sử dụng

### Chạy scraper
```bash
python main.py
```

Hoặc chạy trực tiếp:
```bash
python scraper.py
```

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
| year | Năm | integer |
| asset | Tài sản | float |
| revenue | Doanh thu | float |
| lnst | Lợi nhuận ròng | float |
| vcsh | Vốn chủ sở hữu | float |

## 🔧 Tuỳ chỉnh

### Thay đổi danh sách cổ phiếu
Sửa file `get_hose_stocks.py`:
```python
hose_stocks = ['VCB', 'VIC', 'BID', ...]  # Thêm mã cổ phiếu
```

### Thay đổi năm
Sửa file `main.py`:
```python
scraper.scrape_all_stocks(stocks, years=range(2020, 2026))
```

## 📊 Ví dụ output

```
code    name                           industry  year  asset       revenue     lnst      vcsh
----    ----                           --------  ----  -----       -------     ----      ----
VCB     Vietcombank                    Banking   2020  1500000000  1200000000  150000000 500000000
VCB     Vietcombank                    Banking   2021  1600000000  1300000000  160000000 550000000
```

## ⚠️ Lưu ý

- VietStock có thể block request nếu quá nhanh. Scraper đã có delay (1-2 giây giữa các request)
- Nếu gặp lỗi, hãy kiểm tra:
  - Kết nối internet
  - VietStock có còn hoạt động không
  - API endpoint có thay đổi không
- Log được lưu trong `scraper.log`

## 🐛 Troubleshooting

### Lỗi: "Connection timeout"
```python
# Tăng timeout trong scraper.py
response = self.session.get(url, params=params, timeout=20)  # Từ 10 -> 20
```

### Lỗi: "API endpoint không tìm thấy"
API VietStock có thể đã thay đổi. Kiểm tra:
```bash
curl "https://vietstock.vn/api/Stock/GetListByExchange?exchange=HOSE"
```

## 📈 Cải tiến tương lai

- [ ] Hỗ trợ scrape từ các nguồn khác (SSI, TCBS)
- [ ] Xây dựng database để lưu trữ
- [ ] Dashboard để visualize dữ liệu
- [ ] Scheduling tự động update dữ liệu hàng tháng
- [ ] API để query dữ liệu

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra `scraper.log`
2. Mở GitHub Issue
3. Liên hệ qua email

## 📄 License

MIT License - Tự do sử dụng cho mục đích không lợi nhuận

---

**Last Updated**: 2026-06-01
**Author**: nickphu0001111-eng
