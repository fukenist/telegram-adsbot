import json
import requests
import time
import re
from bs4 import BeautifulSoup
from requests import RequestException


def get_proxy():
    proxy = requests.get(
        'https://gimmeproxy.com/api/getProxy?country=RU&get=true&supportsHttps=true&protocol=http')
    proxy_json = json.loads(proxy.content)
    if proxy.status_code != 200 and 'ip' not in proxy_json:
        raise RequestException
    else:
        return 'http://' + proxy_json['ip'] + ':' + proxy_json['port']

#результат http://176.215.199.70:8080

def get_html(url):
    import random
    USER_AGENTS = [
        'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv)',
        'Chrome/70.0.3538.77 Safari/537.36',
        'Opera/9.68 (X11; Linux i686; en-US) Presto/2.9.344 Version/11.00',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows 95; Trident/5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_6) AppleWebKit/5342 (KHTML, like Gecko) Chrome/37.0.896.0 Mobile Safari/5342',
        'Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/533.49.2 (KHTML, like Gecko) Version/5.0 Safari/533.49.2',
        'Mozilla/5.0 (Windows NT 5.0; sl-SI; rv:1.9.2.20) Gecko/20110831 Firefox/37.0'
    ]
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    proxy = {
        # 'https': get_proxy()
    }
    response = requests.get(url, headers=headers)
    
    return response.content

#результат весь html страницы

html_url = 'https://www.avito.ru/sochi/kvartiry/sdam/na_dlitelnyy_srok/1-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUjlkBRcaaDBV7ImZyb20iOjAsInRvIjoyMDAwMH0&user=1'


def get_ads_list(avito_search_url):
    """
    :param avito_search_url: url like https://www.avito.ru/yalta/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1
    :return: ads list
    """
    html = get_html(avito_search_url)
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find_all('div', {'data-marker': 'item'})  #все рекламы спарсены здесь
    
    ads_list = []
    for ad in ads:
        regex1 = re.compile('iva-item-content.+')
        ad_wrapper = ad.find('div', {'class': regex1})
        ad_wrapper_a = ad_wrapper.find('a', {'data-marker': 'item-title'})
        #print(ad_wrapper)

        ad_id = ad.attrs['data-item-id']
        ad_url = 'https://m.avito.ru' + ad_wrapper_a.attrs['href']
        ad_header = ad_wrapper_a.find('h3').text
        #print(ad_url)
        #print(ad_header)

        regex2 = re.compile('iva-item-priceStep.+')
        ad_price = ad.find('div', {'class': regex2})
        ad_price = ad_price.find('meta', {'itemprop': 'price'})
        ad_price = ad_price.attrs['content']
        

        ad_img = ad_wrapper.find('img', {'itemprop': 'image'})
        
        if ad_img:
            link_img = ad_img.attrs['src']
            print(ad_img.attrs['src'])
        else:
            ad_img = None

        ads_list.append({
            'id' : ad_id,
            'title' : ad_header.replace(u'\xa0', u' '),
            'price' : ad_price.replace(u'\xa0', u' '),
            'url' : ad_url,
            'img' : link_img,
            })

    

    return ads_list



def get_new_ads(new, old):
    _ = []
    for ad in new:
        if ad not in old:
            _.append(ad)
    return _