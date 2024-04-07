import requests
import time
import json
import getpass

def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Print timer on the same line
        time.sleep(1); seconds -= 1
    print('Countdown complete!')

def collect_details():
	email = input("Insert your email or username: ")
	pswd = getpass.getpass("Insert your password: ")

	resp = input("Is the following above correct -> (y/n): ")
	if resp.lower() == "y":
		return email, pswd
	else:
		collect_details()



def login():
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}

	url = "https://faucetearner.org/api.php?act=login"

	email, pwd = collect_details()
	session = requests.Session()
	payload = {"email":email, "password":pwd}
	
	try:
		response = session.post(url, json=payload, headers=headers)
		if response.status_code == 200:
			print("Attempting..")
			text = json.loads(response.text)
			if "wrong" in text["message"]:
				print("Invalid Credentials..")
			else:
				print(f"{text['message']} on user: {email}"); activate_token(session)		
		else:
			print("An error occured while trying to login")
			print(reponse.text)
	except Exception as e:
		print(e)

def activate_token(session):
	count = 0;
	while True:
		url = "https://faucetearner.org/api.php?act=get_faucet"
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
		"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}

		response = session.post(url, headers=headers)
		if response.status_code == 200:
			text = json.loads(response.text)
			collect_token(session); count += 1
			print(text["message"])
			print(f"\nClaims:{count}"); print()
			print("Time-Left"); countdown(60)
		else:
			print("An error occured here..")
			print(response.text)

def collect_token(session):
	url = "https://faucetearner.org/api.php?act=faucet"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
	"X-Requested-With":"XMLHttpRequest", "Content-Type":"application/json"}
	response = session.post(url, headers=headers)
	if response.status_code == 200:
		text = json.loads(response.text)
		print(); print(text["message"])
	else:
		print("An error occured here..")
		print(response.text)
		

login()


