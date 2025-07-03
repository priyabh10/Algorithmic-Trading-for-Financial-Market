# pip install fyers-apiv2
# pip install selenium
# pip install webdriver-manager

from fyers_api.Websocket import ws
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time
import document_file
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import talib as ta
import pandas as pd

log_path = document_file.log_path
client_id = document_file.client_id
secret_key = document_file.secret_key
redirect_url = document_file.redirect_url
response_type = document_file.response_type
grant_type = document_file.grant_type
username = document_file.username
password = document_file.password
pin1 = document_file.pin1
pin2 = document_file.pin2
pin3 = document_file.pin3
pin4 = document_file.pin4

script_list =["HDFCBANK-EQ","SBIN-EQ","INFY-EQ"]

exchange = "NSE"
quantity = int(1)
timeframe = "1"
from_date = "2022-07-10"
today = datetime.datetime.now().strftime('%Y-%m-%d') #"2022-03-14"
rsi_overbought = 80
rsi_oversold = 20
buy_traded_stock = []
sell_traded_stock = []
ma_short = 13
ma_long = 22

def getTime():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def placeOrder(script, order):
	if order == "BUY":
		order = fyers.place_order({"symbol":f"{exchange}:{script}","qty":quantity,"type":"2","side":"1","productType":"INTRADAY","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"})
		print(f"Buy Order Placed for {script} at time: {getTime()}")
	else:
		order = fyers.place_order({"symbol":f"{exchange}:{script}","qty":quantity,"type":"2","side":"-1","productType":"INTRADAY","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"})
		print(f"Sell Order Placed for {script} at time: {getTime()}")

def maAlgorithm():
	for script in script_list:
		data = {"symbol":f"{exchange}:{script}","resolution": timeframe,"date_format":"1","range_from": from_date,"range_to": today,"cont_flag":"0"}
		try:
			hist_data = fyers.history(data)

		except Exception as e:
			raise e
		hist_data = hist_data['candles']
		df = pd.DataFrame(hist_data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
		df['date'] = pd.to_datetime(df['date'], unit = "s", utc=True)
		df['date'] = df['date'].dt.tz_convert('Asia/Kolkata')
		df["rsi"] = ta.RSI(df["close"], timeperiod=14).round(2)
		df["ema_long"] = ta.EMA(df["close"], timeperiod=ma_long).round(2)
		df["ema_short"] = ta.EMA(df["close"], timeperiod=ma_short).round(2)
		df.dropna(inplace=True)
		if not df.empty:
			print(df)
			if (df.ema_short.values[-1] > df.ema_long.values[-1]) and (df.ema_short.values[-2] < df.ema_long.values[-2]) and (script not in sell_traded_stock):
				sell_traded_stock.append(script)
				placeOrder(script, "SELL")

			if (df.ema_short.values[-1] < df.ema_long.values[-1]) and (df.ema_short.values[-2] > df.ema_long.values[-2]) and (script not in buy_traded_stock):
				buy_traded_stock.append(script)
				placeOrder(script, "BUY")

def generate_access_token(auth_code, client_id, secret_key):
    appSession = accessToken.SessionModel(client_id=client_id, secret_key=secret_key, grant_type="authorization_code")
    appSession.set_token(auth_code)
    response = appSession.generate_token()["access_token"]
    return response


def generate_auth_code():
    session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_url,
                                       response_type='code', grant_type='authorization_code')
    response = session.generate_authcode()
    print("login URL", response)
    auth_code = input("Enter auth code :")
    return auth_code

def main():
	global fyers

	auth_code = generate_auth_code()
	access_token = generate_access_token(auth_code, client_id, secret_key)
	fyers = fyersModel.FyersModel(token=access_token, log_path=log_path, client_id=client_id)
	fyers.token = access_token
	newtoken = f"{client_id}:{access_token}"
	data_type = "symbolData"

	closingtime = int(15) * 60 + int(10)
	orderplacetime = int(9) * 60 + int(20)
	print("Closing time",closingtime)
	timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Waiting for 9.20 AM , Time Now:{getTime()}")

	while timenow < orderplacetime:
		time.sleep(0.2)
		timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Ready for trading, Time Now:{getTime()}")


	while timenow < closingtime:
		maAlgorithm()

if __name__ == "__main__":
	main()