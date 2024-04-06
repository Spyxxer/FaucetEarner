import requests
import json
import threading
import time

def process_withdrawal(session, address, tag):
	url = "https://faucetearner.org/api.php?act=withdraw"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}
	payload = {"amount":"", "eth_address":None, "tag":tag, "wallet":address}
	response = session.post(url, json=, headers=headers)
	if response.status_code == 200:
		print(f"withdrawing to address [{address}]..")
		print(response.text)
	else:
		print(response.text)


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
		print(reponse.text)


def collect_details():
	email = input("Insert your email or username: ")
	pswd = input("Insert your password: ")

	resp = input("Is the following above correct -> (y/n):")
	if resp.lower() == "y":
		return email, pswd
	else:
		collect_details()

def withdraw_func():
	address = input("Please insert address: ")
	tag = input("Please insert memo/tag: ")
	ans = input("Please Is the following above correct > [y/n]: ")
	if ans.lower() == "y":
		withdraw_type = input("Insert withdrawal type -> [single/multiple]")
		if withdraw_type == "single":
			user, password = collect_details()
			login(user, password, address, tag)
		elif withdraw_type == "multiple":
			with open("logins.txt", "r") as file:
				for line in file:
    				line = line.strip()
    				user, mail, pwd = line.split(" ")
    				thread = threading.Thread(target=login, args=(user, pwd, address, tag))
    				thread.start(); time.sleep(5)
    	else:
    		print("INVALID RESPONSE!"); withdraw_func()
	else:
		withdraw_func()

withdraw_func()