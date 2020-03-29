import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json
import time
from datetime import date
import matplotlib.pyplot as plt
import uuid 
from getcases import GetCases
#from multiprocessing import Pool
from filelock import Timeout, FileLock
from torch.multiprocessing import Pool, Process, set_start_method, freeze_support

# Get all of the counties
with open("C:/Users/NathanGrant/Downloads/rona/rona/cord_dict.json") as f:
    county_dict = json.load(f)
cases_dict = {}
getcases = GetCases()

def parse_html(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    # kill all script and style elements
    spans = soup.findAll("span", {"class": "st"})
    spans = [str(s).lower() for s in spans]
    spans = [re.sub("<.*?>", "", s) for s in spans]
    
    return spans

def get_news(county):
    query = '''"total" "coronavirus" "deaths" "0...500" in ''' + county +" County"
    query = query.replace(' ', '+')
    URL = "https://google.com/search?q=" + query
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(URL, headers=headers)
    print(URL)
    if page.status_code == 200: 
        return parse_html(page)
    else:
        return []
    
def get_cases(county):
    delays = [25, 24, 12, 18, 20, 38]
    delay = np.random.choice(delays)
    time.sleep(delay)

    news_list = get_news(county)
    if len(news_list) > 0:
        scraped_cases = []
        for news in news_list[:4]:
            scraped_cases.append(getcases.predict(news, county))

        num_cases = max(scraped_cases)

        path = "C:/Users/NathanGrant/Downloads/rona/rona/cases_dict.json"
        lock_path = "C:/Users/NathanGrant/Downloads/rona/rona/cases_dict.json.lock"
        lock = FileLock(lock_path, timeout=1)
        with lock:
            with open(path) as json_file:
                json_decoded = json.load(json_file)
        
        if county in json_decoded.keys():
            json_decoded[county].append([county_dict[county][0],county_dict[county][1], num_cases, date.today().strftime("%m/%d/%y")])
        else:
            json_decoded[county] = [[county_dict[county][0],county_dict[county][1], num_cases, date.today().strftime("%m/%d/%y")]]

        with lock:
            with open(path, 'w') as json_file:
                json.dump(json_decoded, json_file)
        print(county, num_cases)
        return max(scraped_cases)
    else:
        print("Blocked")
        return 0

if __name__ == '__main__':
    counties = list(county_dict.keys())
    
    print(len(counties))
    freeze_support()

    try:
        set_start_method('spawn')
    except RuntimeError:
        pass

    p = Pool(4)
    records = p.map(get_cases, counties)
    p.close()
    p.join()
