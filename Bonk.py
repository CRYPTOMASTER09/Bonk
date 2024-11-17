import requests
import json
import os
from urllib.parse import parse_qs, unquote
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Boinkers:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'boink.boinkers.co',
            'Origin': 'https://boink.boinkers.co',
            'Pragma': 'no-cache',
            'Referer': 'https://boink.boinkers.co/upgrade-boinker',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Safari/537.36 Edg/128.0.0.0'
        }
        self.token_file = 'tokens.json'

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Boinkers Script by {Fore.BLUE + Style.BRIGHT} CRYPTO MASTER 
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Join Script Channel:- {Fore.YELLOW + Style.BRIGHT}https://t.me/airdropconfirm97
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def extract_user_data(self, query: str) -> str:
        parsed_query = parse_qs(query)
        user_data = parsed_query.get('user', [None])[0]

        if user_data:
            user_json = json.loads(unquote(user_data))
            return str(user_json.get('first_name', 'Unknown'))
        return 'Unknown'

    def load_tokens(self):
        try:
            if not os.path.exists('tokens.json'):
                return {"accounts": []}

            with open('tokens.json', 'r') as file:
                data = json.load(file)
                if "accounts" not in data:
                    return {"accounts": []}
                return data
        except json.JSONDecodeError:
            return {"accounts": []}

    def save_tokens(self, tokens):
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)

    def generate_tokens(self, queries: list):
        tokens_data = self.load_tokens()
        accounts = tokens_data["accounts"]

        for idx, query in enumerate(queries):
            account_name = self.extract_user_data(query)

            existing_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)

            if not existing_account:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Token Is None{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Generating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)

                token = self.users_login(query)
                if token:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )
                    accounts.insert(idx, {"first_name": account_name, "token": token})
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Query Is Expired{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

        self.save_tokens({"accounts": accounts})

    def renew_token(self, account_name):
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        
        account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if account and "token" in account:
            token = account["token"]
            if not self.users_me(token):
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Token Isn't Valid{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Regenerating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)
                
                accounts = [acc for acc in accounts if acc["first_name"] != account_name]
                
                query = next((query for query in self.load_queries() if self.extract_user_data(query) == account_name), None)
                if query:
                    new_token = self.users_login(query)
                    if new_token:
                        accounts.append({"first_name": account_name, "token": new_token})
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Query Is Valid{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Query Is Expired{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Query Is None. Skipping {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
        
        self.save_tokens({"accounts": accounts})

    def load_queries(self):
        with open('query.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def users_login(self, query: str, retries=3):
        url = 'https://boink.boinkers.co/public/users/loginByTelegram?tgWebAppStartParam=boink1493482017&p=android'
        data = json.dumps({"initDataString":query, "sessionParams":{}})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()['token']
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def users_me(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/users/me?p=android'
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None

    def claim_booster(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/boinkers/addShitBooster?p=android'
        data = json.dumps({'multiplier':2, 'optionNumber':1})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None

    def claim_inbox(self, token: str, message_id: str, retries=3):
        url = 'https://boink.boinkers.co/api/inboxMessages/claimInboxMessagePrize?p=android'
        data = json.dumps({'inboxMessageId':message_id})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def tasks(self, token: str, retries=3):
        url = 'https://boink.boinkers.co/api/rewardedActions/getRewardedActionList?p=android'
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def start_tasks(self, token: str, name_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/rewardedActions/rewardedActionClicked/{name_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def claim_tasks(self, token: str, name_id: str, retries=3):
        url = f'https://boink.boinkers.co/api/rewardedActions/claimRewardedAction/{name_id}?p=android'
        data = {}
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, json=data, timeout=10)
                if response.status_code == 200:
                    try:
                        return response.json()
                    except requests.JSONDecodeError:
                        return None
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def watch_ads(self, token: str, key: str, retries=3):
        url = 'https://boink.boinkers.co/api/rewardedActions/ad-watched?p=android'
        data = json.dumps({'adsForSpins':False, 'providerId':key})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while attempt < retries:
            try:
                response = self.session.post(url, headers=self.headers, data=data, timeout=10)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except (requests.Timeout, requests.ConnectionError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Retrying {attempt+1}/{retries} {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
            attempt += 1
            time.sleep(2)

        return None
        
    def spin_wheel(self, token: str, game_type: str, id: str, multiplier: str, retries=3):
        url = f'https://boink.boinkers.co/api/play/spin{game_type.capitalize()}/{multiplier}?p=android'
        data = json.dumps({'liveOpId':id} if id else {})
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json'
        })

        attempt = 0
        while att
