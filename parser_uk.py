from bs4 import BeautifulSoup
import requests
import re
import json

URL = 'https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=TRUE&postcode=WC2N+5DU&make=TESLA&price-search-type=total-price'

HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'accept' : '*/*'
}
file_name = ("uk_cars" + ".json")
full_json = {}
request = requests.get(URL, headers=HEADERS).content
soup = BeautifulSoup(request, 'lxml')
container = soup.select("li.search-page__result")

def record_to_json( file_name):
    names_list = []
    container_names = soup.select('div.information-container h2 a')
    for name in container_names:
        str_name = name.text
        name = str_name.strip()
        #print(name)
        names_list.append(name)

    links = []
    container_links = soup.select('div.information-container h2 a')
    for i in container_links:
        ii = i['href'].split("?")[0]
        link = ("https://www.autotrader.co.uk" + ii)
        links.append(link)
        #print(link)

    photos = []
    container_photo = soup.select('figure.listing-main-image a img')
    for link_photo in container_photo:
        photos.append(link_photo['src'])
        #print(link_photo['src'])

    list_price = []
    container_text = soup.find_all("a", attrs={ "class" : "js-click-handler listing-fpa-link listings-price-link tracking-standard-link"})
    for i in container_text:
        pr = i.find_all("div", attrs={ "class" : "vehicle-price"})
        str_price = "".join((re.findall(r'[0-9]{,3},[0-9]{,3}', str(pr))))
        price =27*int(str_price.replace(',', ''))
        list_price.append(price)
        #print(price)

    for n, l, f, p in zip(names_list, links, photos, list_price):
        to_json = {n:{'head': n, 'link': l, 'photo': f, 'price': p}}
        full_json.update(to_json)

    with open(file_name, 'w') as f:
        json.dump(full_json, f)
    with open(file_name) as f:
        print(f.read())