import requests
import json
import threading
import time, re

def process_amount(session):
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
		return float(pamt)
	else:
		print("Status_CODE:", response_load.status_code)
	

def login(email, password, c):
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}

	url = "https://faucetearner.org/api.php?act=login"

	
	session = requests.Session()

	payload = {"email":email, "password":password}
	response = session.post(url, json=payload, headers=headers)

	if response.status_code == 200:
		print(f"Attempting {c}..")
		text = json.loads(response.text)
		if "wrong" in text["message"]:
			print(f"Invalid Credentials.. on line {c}")
			return "End"
		else:
			print(f"{text['message']} on user: {email}"); 
			return process_amount(session)	
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

def check_func():
	total = 0; count = 1
	with open("user_data.txt", "r") as file:
		for line in file:
			line = line.strip()
			user, mail, pwd, address, tag = line.split(" ")
			value = login(user, pwd, count)
			if isinstance(value, float):
				total += value
				print("Amount in account: ", value); print("Current Total is: ", total)
			elif value == "End":
				break
			else:
				print("Value Found: ", value);
			count += 1
			if count > 3:
				break
	print("Total Amount Found: ", total)

check_func()