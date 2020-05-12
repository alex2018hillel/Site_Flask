from libs.car import Cars
from libs.database import db_session
# import libs.car
import requests
from bs4 import BeautifulSoup
import re

file_name = ("olx" + ".csv")
URL = 'http://www.olx.ua/transport/legkovye-avtomobili/q-электромобиль/'
HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'accept' : '*/*'
    }

request = requests.get(URL, headers=HEADERS).content
soup = BeautifulSoup(request, 'lxml')


def parser():
    list_price = []
    container = soup.select("td.offer")
    for c in container:
        container_text = c.find_all("div", attrs={ "class" : "space inlblk rel"})
        price = "".join((re.findall(r'[0-9]{,3} [0-9]{,3} [0-9]{,3}', str(container_text))))
        list_price.append(price)

        names_list = []
        container_names = soup.select('div.offer-wrapper table tbody tr td.title-cell div h3 a strong')
        for name in container_names:
            # print(name.text)
            names_list.append(name.text)
    #----------------------------------------------------------------
    links = []
    container_links = soup.select('div.offer-wrapper table tbody tr td.photo-cell a')
    for link in container_links:
        links.append(link['href'])
    #---------------------------------------------
    photos = []
    container_photo = soup.select('div.offer-wrapper table tbody tr td.photo-cell a img')
    for link_photo in container_photo:
        photos.append(link_photo['src'])


    def record_to_db(file_name):
        myfile = open(file_name, 'w', encoding='cp1251')
        for n, l, f, p in zip(names_list, links, photos, list_price):
            # db_session.add(1,2,3,4)
            #
            # libs.car.add_cars(n, l, f, p)
            db_session.add(Cars(n, l, f, p))
            db_session.commit()

            try:
                line = '{}{}{}{}{}'.format(n, '\t', l, '\t', f, '\t', str(p))
                myfile.write(line+'\n')
            except:
                pass


    record_to_db(file_name)
parser()
