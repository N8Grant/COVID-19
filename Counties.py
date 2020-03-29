import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from multiprocessing import Pool
import time
import json
from filelock import Timeout, FileLock

def get_cord(cn):
    time.sleep(30)
    query = "Coordinates of " + cn +" County"
    query = query.replace(' ', '+')
    URL = "https://google.com/search?q=" + query
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(URL, headers=headers)
    x = 0
    y = 0
    if page.status_code == 200: 
        soup = BeautifulSoup(page.content, 'html.parser')
        divs = soup.findAll("div", {"class": "Z0LcW"})
        cords = [str(l) for l in divs]
        cords = [re.sub("<.*?>", "", s) for s in cords]
        if len(cords) > 0:
            cord_string = cords[0]
            cord_l = re.sub("° [A-Z],?", "", cord_string)
            cord_l = cord_l.split(" ")
            x = cord_l[1]
            y = cord_l[0]
            print([cn, x, y])       
    else:
        print("Couldnt find it")
    path = "C:/Users/NathanGrant/Downloads/rona/rona/cord_dict.json"
    lock_path = "C:/Users/NathanGrant/Downloads/rona/rona/cord_dict.json.lock"
    lock = FileLock(lock_path, timeout=1)
    with lock:
        with open(path) as json_file:
            json_decoded = json.load(json_file)
        
    json_decoded[cn] = [x,y]

    with lock:
        with open(path, 'w') as json_file:
            json.dump(json_decoded, json_file)
       

if __name__ == '__main__':
    df = pd.read_csv("C:/Users/NathanGrant/Downloads/rona/rona/counties.csv")
    county_dict = df['County Names'].to_dict()
    counties = []
    for row in county_dict:
        counties.append(county_dict[row])

    p = Pool(10)
    records = p.map(get_cord, counties)
    p.terminate()
    p.join()

    cord_dict = {}
    for l in records:
        cord_dict[l[0]] = [l[1],l[2]]

    json = json.dumps(cord_dict)
    f = open("C:/Users/NathanGrant/Downloads/rona/rona/cord_dict.json","w")
    f.write(json)
    f.close()

