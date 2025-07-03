# pip install fyers-apiv2
# pip install selenium
# pip install webdriver-manager
# pip install pandas
# pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

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

script_list = ["HDFCBANK-EQ","SBIN-EQ","INFY-EQ","ICICIBANK-EQ","AXISBANK-EQ","MARUTI-EQ","WIPRO-EQ","BHARTIARTL-EQ","ASIANPAINT-EQ","DIVISLAB-EQ","HDFC-EQ","HCLTECH-EQ","TECHM-EQ","KOTAKBANK-EQ","TITAN-EQ","TATACONSUM-EQ","LT-EQ","UPL-EQ","ITC-EQ","EICHERMOT-EQ","TCS-EQ","ADANIPORTS-EQ","CIPLA-EQ","SBILIFE-EQ","DRREDDY-EQ","RELIANCE-EQ","ULTRACEMCO-EQ","M&M-EQ","BAJAJFINSV-EQ","GRASIM-EQ","NESTLEIND-EQ","INDUSINDBK-EQ","HEROMOTOCO-EQ","POWERGRID-EQ","NTPC-EQ","BRITANNIA-EQ","SUNPHARMA-EQ","BAJAJ-AUTO-EQ","BAJFINANCE-EQ","HINDALCO-EQ","BPCL-EQ","SHREECEM-EQ","TATASTEEL-EQ","JSWSTEEL-EQ","HDFCLIFE-EQ","COALINDIA-EQ","HINDUNILVR-EQ","TATAMOTORS-EQ","IOC-EQ","ONGC-EQ"]

exchange = "NSE"
quantity = int(100)
timeframe = "15"
from_date = "2022-03-10"
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
		df = pd.DataFrame(hist_data["candles"], columns=['date', 'open', 'high', 'low', 'close', 'volume'])
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

def generate_access_token(auth_code, appId, secret_key):
	appSession = accessToken.SessionModel(client_id=appId, secret_key=secret_key,grant_type="authorization_code")
	appSession.set_token(auth_code)
	response = appSession.generate_token()["access_token"]
	return response

def generate_auth_code():
	url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=state&scope=&nonce="
	driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
	# driver = webdriver.Firefox(executable_path=r"C:\Users\tradi\.wdm\drivers\geckodriver\win64\v0.30.0\geckodriver.exe")
	driver.get(url)
	time.sleep(8)
	driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
	driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
	time.sleep(8)
	driver.execute_script(f"document.querySelector('[id=fy_client_pwd]').value = '{password}'")
	driver.execute_script("document.querySelector('[id=loginSubmit]').click()")
	time.sleep(8)
	driver.find_element_by_id("verify-pin-page").find_element_by_id("first").send_keys(pin1)
	driver.find_element_by_id("verify-pin-page").find_element_by_id("second").send_keys(pin2)
	driver.find_element_by_id("verify-pin-page").find_element_by_id("third").send_keys(pin3)
	driver.find_element_by_id("verify-pin-page").find_element_by_id("fourth").send_keys(pin4)
	driver.execute_script("document.querySelector('[id=verifyPinSubmit]').click()")
	time.sleep(8)
	newurl = driver.current_url
	auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
	driver.quit()
	return auth_code

def main():
	global fyers

	auth_code = generate_auth_code()
	access_token = generate_access_token(auth_code, client_id, secret_key)
	fyers = fyersModel.FyersModel(token=access_token, log_path=log_path, client_id=client_id)
	fyers.token = access_token

	closingtime = int(15) * 60 + int(10)
	orderplacetime = int(9) * 60 + int(20)
	timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Waiting for 9.20 AM , Time Now:{getTime()}")

	while timenow < orderplacetime:
		time.sleep(0.2)
		timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
	print(f"Ready for trading, Time Now:{getTime()}")

	while timenow < closingtime:
		rsiAlgorithm()

if __name__ == "__main__":
	main()