# pip install fyers-apiv2
# pip install selenium
# pip install webdriver-manager
# pip install pandas
# pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import os

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

#from final import generate_auth_code, generate_access_token, log_path

client_id = '8S56FEB6JI-100'
secret_key = 'BGOWTLDD3I'
redirect_url = 'http://127.0.0.1:5000/login'
log_path = os.getcwd()
script_list = ["HDFCBANK-EQ","SBIN-EQ","INFY-EQ"]
exchange = "NSE"
quantity = int(1)
timeframe = "1"
from_date = "2022-07-10"
today = datetime.datetime.now().strftime('%Y-%m-%d') #"2022-03-14"
rsi_overbought = 80
rsi_oversold = 20
buy_traded_stock = []
sell_traded_stock = []

def getTime():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def placeOrder(script, order):
	if order == "BUY":
		order = fyers.place_order({"symbol":f"{exchange}:{script}","qty":quantity,"type":"2","side":"1","productType":"INTRADAY","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"})
		print(f"Buy Order Placed for {script} at time: {getTime()}")
	else:
		order = fyers.place_order({"symbol":f"{exchange}:{script}","qty":quantity,"type":"2","side":"-1","productType":"INTRADAY","limitPrice":"0","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"})
		print(f"Buy Order Placed for {script} at time: {getTime()}")

def rsiAlgorithm():
	for script in script_list:
		data = {"symbol":f"{exchange}:{script}","resolution": timeframe,"date_format":"1","range_from": from_date,"range_to": today,"cont_flag":"0"}
		try:
			hist_data = fyers.history(data)

		except Exception as e:
			raise e
		hist_data = hist_data['candles']
		df=pd.DataFrame(hist_data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

		df['date'] = pd.to_datetime(df['date'], unit = "s", utc=True)
		df['date'] = df['date'].dt.tz_convert('Asia/Kolkata')
		df["rsi"] = ta.RSI(df["close"], timeperiod=14).round(2)

		df.dropna(inplace=True)
		if not df.empty:
			rsi_value = df.rsi.values[-1]
			# print(df)
			if (rsi_value >= rsi_overbought) and (script not in sell_traded_stock):
				sell_traded_stock.append(script)
				placeOrder(script, "SELL")

			if (rsi_value <= rsi_oversold) and (script not in buy_traded_stock):
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


	orderplacetime = int(9) * 60 + int(20)
	closingtime = int(13) * 60 + int(35)
	print("close",closingtime)
	timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Waiting for 9.20 AM , Time Now:{getTime()}")

	while timenow < orderplacetime:
		time.sleep(0.2)
		timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Ready for trading, Time Now:{getTime()}")
	fs = ws.FyersSocket(access_token=newtoken, run_background=False, log_path=log_path)
	fs.websocket_data = placeOrder
	fs.subscribe(symbol=script_list, data_type=data_type)
	fs.keep_running()




	while timenow < closingtime:
		rsiAlgorithm()



if __name__ == "__main__":
	main()