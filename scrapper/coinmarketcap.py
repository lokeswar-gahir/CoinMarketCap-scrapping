from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
from bs4 import BeautifulSoup as bs
import json
from .models import Task
from dotenv import load_dotenv
import os

load_dotenv('.env')

class CoinMarketCap:
    def __init__(self):
        self.url = None
        self.headers = None
        self.task=None
        self.json_data=None
        self.valid_coins=None

    def save_valid_cryptos(self, limit: int=100 ,file: str='scrapper\\resources\\crypto_symbols.txt'):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start': '1',
        'limit': limit,
        'convert': 'USD'
        }
        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            with open(file, 'w', encoding='utf-8') as f:
                for item in data['data']:
                    f.write(item['symbol']+'\n')
            print(f'Data Saved to \'{file}\'')
        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            print(e)

    def add_additionals(self, dict_buffer):
        site = f'https://coinmarketcap.com/currencies/{dict_buffer["slug"]}/'
        res = requests.get(site)
        soup = bs(res.content, 'html.parser')
        header = soup.find('div', attrs={'id':'section-coin-overview'})
        price_change = header.find_all('div', recursive=False)[1].div.p
        price_change_val = price_change.text.split()[0]
        change = price_change_val.replace("%", "")
        if price_change['color'] == 'red':
            change = float(change) * (-1)
        dict_buffer['output']['price_change'] = float(change)

        coin_overview = soup.find('div', attrs={'id':'section-coin-stats'})

        stat_divs = coin_overview.dl.find_all('div', recursive=False)
        dict_buffer["output"]['volume_rank']=stat_divs[1].text.split("#")[-1]

        dict_buffer['output']['contracts']=None
        dict_buffer['output']['official_links']=None
        dict_buffer['output']['socials']=None

        link_boxes = coin_overview.parent.find_all('div', recursive=False)[1]
        link_boxes = list(link_boxes)
        required_boxes=list()
        required_boxes.append(link_boxes[0])
        required_boxes.append(link_boxes[1])
        required_boxes.append(link_boxes[2])
        for box in required_boxes:
            if 'Contracts' in box.text:
                contract_link = box.a['href']
                contract_company_name = box.a.span.text
                contract_company_name = contract_company_name.replace(":", "").strip()
                dict_buffer['output']['contracts'] = [{"name": contract_company_name, "address": contract_link}]
            elif 'Official links' in box.text:
                inner_box = box.find_all('div', recursive=False)[1]
                inner_links = inner_box.div.find_all('div', recursive=False)
                official_links_list = list()
                for inner_link in inner_links:
                    if inner_link.find('a'):
                        current_link = inner_link.a['href']
                        current_text = inner_link.a.text.strip()
                        official_links_list.append({"name":current_text, "link": current_link})
                dict_buffer['output']['official_links'] = official_links_list
            elif 'Socials' in box.text:
                # print('\nSocials:')
                inner_box = box.find_all('div', recursive=False)[1]
                inner_links = inner_box.div.find_all('div', recursive=False)
                social_links_list = list()
                for inner_link in inner_links:
                    if inner_link.find('a'):
                        current_link = inner_link.a['href']
                        current_text = inner_link.a.text.replace("𝕏","").strip()
                        # print(current_text, ":", current_link)
                        social_links_list.append({"name": current_text, "url": current_link})
                dict_buffer['output']['socials']=social_links_list

        return dict_buffer

    def make_request(self, valid_coins:list):
        self.url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        self.headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get("API_KEY"),
        }
        parameters = {
            'symbol': ",".join(valid_coins)
        }
        self.valid_coins = valid_coins
        session = Session()
        session.headers.update(self.headers)
        try:
            response = session.get(self.url, params=parameters)
            self.json_data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            print('Error while fetching API data !!!')
            print(e)

    def scrap_and_process_data(self):
        try:
            self.task = list()
            for coin in self.valid_coins:
                outer_dict=dict()
                outer_dict['coin']=coin

                inner_dict = dict() # output dict
                actual_data = self.json_data['data'][coin][0]
                outer_dict['slug']=actual_data['slug']

                inner_dict['circulating_supply'] = actual_data['circulating_supply']
                inner_dict['total_supply'] = actual_data['total_supply']
                inner_dict['market_cap_rank'] = actual_data['cmc_rank']
                inner_json_data = actual_data['quote']['USD']
                inner_dict['price']=inner_json_data['price']
                inner_dict['market_cap']=inner_json_data['market_cap']
                inner_dict['volume'] = inner_json_data['volume_24h']
                inner_dict['volume_change'] = inner_json_data['volume_change_24h']
                # dict1['volume_change']=round((dict1['volume']/dict1['market_cap'])*100, 2)
                inner_dict['diluted_market_cap']=inner_json_data['fully_diluted_market_cap']

                outer_dict['output'] = inner_dict
                outer_dict = self.add_additionals(outer_dict)
                self.task.append(outer_dict)

            # print(json.dumps(task))
        except Exception as e:
            print(e)

    def final_output(self):
        self.url = None
        self.headers = None
        self.json_data=None
        self.valid_coins=None
        return json.dumps(self.task)
    
    @staticmethod
    def get_results(job_id):
        query_set = Task.objects.filter(job__job_id=job_id)
        if len(query_set)!=0:
            task = [{"coin":coin.coin ,"output":coin.data} for coin in query_set]
            return task

if __name__ == '__main__':
    c = CoinMarketCap()
    c.make_request(['DUKO','ETH'])
    c.scrap_and_process_data()
    print(c.send_back())
