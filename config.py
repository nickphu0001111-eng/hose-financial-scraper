# Cấu hình chung

# VietStock
VIETSTOCK_BASE_URL = "https://vietstock.vn"
VIETSTOCK_API_URL = "https://vietstock.vn/api"

# Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Timeout
REQUEST_TIMEOUT = 10
RETRY_ATTEMPT = 3
RETRY_DELAY = 2000  # milliseconds

# Scraper settings
DELAY_BETWEEN_REQUESTS = 1  # giây
DELAY_BETWEEN_STOCKS = 2    # giây

# Data
YEARS = range(2020, 2026)
FINANCIAL_FIELDS = ['asset', 'revenue', 'lnst', 'vcsh']

# Output
OUTPUT_DIR = 'output'
OUTPUT_FORMAT = 'both'  # 'csv', 'excel', 'both'

# Logging
LOG_FILE = 'scraper.log'
LOG_LEVEL = 'INFO'
