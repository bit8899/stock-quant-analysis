# -*- coding: utf-8 -*-
import pandas as pd
import talib
import tushare as ts
from datetime import datetime, timedelta
import os

# ===================== Replace with your Tushare Token =====================
TOKEN = "c796905ebfce0961493c222d2dd4b81a1169c54b173bfa8008140397"  # Example: TOKEN = "1234567890abcdef1234567890abcdef"
STOCK_CODE = "600519.SH"  # Moutai stock code
DAYS = 30  # Analyze 30 days data

# ===================== 1. Initialize Tushare =====================
ts.set_token(TOKEN)
pro = ts.pro_api()

# ===================== 2. Get real stock data =====================
end_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=DAYS)).strftime("%Y%m%d")

print(f"Getting data for {STOCK_CODE} from {start_date} to {end_date}...")
df = pro.daily(
    ts_code=STOCK_CODE,
    start_date=start_date,
    end_date=end_date
)

# ===================== 3. Data check and analysis =====================
if df.empty:
    print("⚠️ No data found! Check:")
    print("1. Token is correct")
    print("2. Date range is reasonable (try DAYS=60)")
else:
    df = df.sort_values(by="trade_date").reset_index(drop=True)
    
    # Calculate indicators
    close = df["close"].values
    df["ma5"] = talib.MA(close, timeperiod=5)
    df["macd"], df["macdsignal"], _ = talib.MACD(close)
    
    latest = df.iloc[-1]
    
    # ===================== 4. Output report =====================
    print("\n===== Moutai (600519) Quantitative Analysis Report =====")
    print(f"Latest trade date: {latest['trade_date']}")
    print(f"Latest close price: {latest['close']:.2f} CNY")
    print(f"5-day MA: {latest['ma5']:.2f} CNY")
    print(f"MACD value: {latest['macd']:.4f}")
    print(f"MACD signal: {latest['macdsignal']:.4f}")
    print(f"Trading signal: {'✅ MACD Golden Cross (Buy)' if latest['macd'] > latest['macdsignal'] else '❌ MACD Death Cross (Hold)'}")
    
    # ===================== 5. Save to local =====================
    df.to_csv("600519_quant_analysis.csv", index=False)
    print(f"\n✅ Result saved to: 600519_quant_analysis.csv")
    
    # ===================== 6. Push to GitHub =====================
    os.system('git config --global user.name "bit8899"')
    os.system('git config --global user.email "bit8899@163.com"')
    os.system("git add .")
    os.system('git commit -m "Add Moutai quantitative analysis result"')
    os.system("git push origin main")
    
    print("✅ Result pushed to GitHub repository!")
    print("🔗 Repository URL: https://github.com/bit8899/stock-quant-analysis")
