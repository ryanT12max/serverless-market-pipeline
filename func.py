import io
import json
import requests
import oracledb
from datetime import datetime
from fdk import response

def get_market_data():
    tickers = ["SPY", "AAPL", "MSFT"]
    market_data = []
    
    for ticker in tickers:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()['chart']['result'][0]['meta']
            market_data.append({
                "ticker": ticker,
                "price": data.get('regularMarketPrice', 0),
                "high": data.get('regularMarketDayHigh', 0),
                "low": data.get('regularMarketDayLow', 0),
                "volume": data.get('regularMarketVolume', 0)
            })
    return market_data

def load_data_to_oracle(market_data):
    connection = oracledb.connect(
        user="ADMIN",
        password="0n@stR8l1n3U", 
        dsn="AviationDB_high",   
        config_dir="/function/wallet",
        wallet_location="/function/wallet",
        wallet_password="Tij79268*"
    )
    
    cursor = connection.cursor()
    sql = """INSERT INTO FINANCIAL_METRICS 
             (TICKER, RECORD_TIME, CURRENT_PRICE, DAY_HIGH, DAY_LOW, VOLUME) 
             VALUES (:1, :2, :3, :4, :5, :6)"""
             
    current_time = datetime.now()
    
    for item in market_data:
        cursor.execute(sql, [
            item['ticker'], current_time, item['price'], 
            item['high'], item['low'], item['volume']
        ])
        
    connection.commit()
    cursor.close()
    connection.close()

def handler(ctx, data: io.BytesIO = None):
    try:
        data = get_market_data()
        if data:
            load_data_to_oracle(data)
        return response.Response(
            ctx, response_data=json.dumps({"status": "Market data loaded successfully"}),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return response.Response(
            ctx, response_data=json.dumps({"error": str(e)}),
            headers={"Content-Type": "application/json"}
        )
