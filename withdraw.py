import requests
import json
import threading
import time, re

def process_withdrawal(session, address, tag):
	url = "https://faucetearner.org/api.php?act=withdraw"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}
	url_load = "https://faucetearner.org/withdraw.php"
	response_load = session.get(url_load, headers=headers)
	if response_load.status_code == 200:
		text = response_load.text
		pattern = r'value="(\d*\.\d+)"'

		# Search for floating point numbers in the text
		pamt = re.findall(pattern, text)[0] 
		payload = {"amount":pamt, "eth_address":None, "tag":tag, "wallet":address}
		response = session.post(url, json=payload, headers=headers)
		if response.status_code == 200:
			print(f"withdrawing to address [{address}]..")
			text = json.loads(response.text)["message"]
			print(text)
		else:
			print(response.text)
	else:
		print("Status_CODE:", response_load.status_code)
	

def login(email, password, address, tag):
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}

	url = "https://faucetearner.org/api.php?act=login"

	
	session = requests.Session()

	payload = {"email":email, "password":password}
	response = session.post(url, json=payload, headers=headers)

	if response.status_code == 200:
		print("Login Successful..")	
		process_withdrawal(session, address, tag)	
	else:
		print("An error occured while trying to login")
		print(response.text)


def collect_details():
	email = input("Insert your email or username: ")
	pswd = input("Insert your password: ")

	resp = input("Is the following above correct -> (y/n): ")
	if resp.lower() == "y":
		return email, pswd
	else:
		collect_details()

def withdraw_func():
	withdraw_type = input("Insert withdrawal type -> [single/multiple]: ")
	if withdraw_type == "single":
		address = input("Please insert address: ")
		tag = input("Please insert memo/tag: ")
		ans = input("Is the following above correct > [y/n]: ")
		if ans.lower() == "y":
			user, password = collect_details()
			login(user, password, address, tag)
		else:
			withdraw_func()
	elif withdraw_type == "multiple":
		i = 1; req = 3;
		with open("user_data.txt", "r") as file:
			for line in file:
				line = line.strip()
				user, mail, pwd, address, tag = line.split(" ")
				thread = threading.Thread(target=login, args=(user, pwd, address, tag))
				thread.start(); time.sleep(5)
				i += 1
				if i > 3:
					break
	else:
		print("Invalid RESPONSE!"); withdraw_func()

withdraw_func()