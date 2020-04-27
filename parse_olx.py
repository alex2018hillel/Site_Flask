import contextlib

import requests
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import lxml.html as lxml
from bs4 import BeautifulSoup
import re
import psycopg2
from psycopg2 import sql
from contextlib import closing
from sqlalchemy import MetaData, create_engine, Table

URL = 'http://www.olx.ua/transport/legkovye-avtomobili/q-электромобиль/'
HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'accept' : '*/*'
    }

request = requests.get(URL, headers=HEADERS).content
soup = BeautifulSoup(request, 'lxml')
parce = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'site_flask',
    'host': 'localhost',
    'port': '5432',
}
parce.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
db = SQLAlchemy(parce)

# db.session.delete(me)
# db.session.commit()


# meta = MetaData()
# with contextlib.closing(psycopg2.connect()) as con:
#     trans = con.begin()
#     for table in reversed(meta.sorted_tables): con.execute(table.delete())
#     trans.commit()
# db.metadata.drop_all()
# db.session.configure(bind=engine)



class Cars(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(1024), nullable=False)
    link = db.Column(db.String(1024), nullable=False)
    photo = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.String(1024), nullable=False)

    def __init__(self, head, link, photo, price):
        self.head = head.strip()
        self.link = link.strip()
        self.photo = photo.strip()
        self.price = price.strip()
# m = MetaData()
# table = Cars(a,a,a,a)
# db.drop(engine)
#db.drop(engine)
deleted_objects = Cars.__table__.delete()
engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES, echo=False)
#ddddd = db.delete('table')
# where(addresses.c.email_address.startswith('xyz%'))
engine.execute(deleted_objects)

db.create_all()
# db.session.add(Message(text, tag, data1))
# db.session.commit()
#-----------------------------------------------------------
# conn = psycopg2.connect(
#     database="site_flask",
#     user="postgres",
#     password="123",
#     host="localhost",
#     port="5432"
# )
# #==========
# #with conn.cursor() as cursor:
# #     conn.autocommit = True
# #==========
# cur = conn.cursor()
# cur.execute('''CREATE TABLE OLD_CARS
#      (head TEXT PRIMARY KEY NOT NULL,
#      link TEXT NOT NULL,
#      photo TEXT NOT NULL,
#      price CHAR(50))''')
# #============================================================================
# with closing(psycopg2.connect(dbname='site_flask', user='postgres',
#                               password='123', host='localhost')) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * FROM OLD_CARS LIMIT 50')
#         for row in cursor:
#             print(row)

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


    def record_to_db(container, file_name):
        myfile = open(file_name, 'w', encoding='cp1251')
        for n, l, f, p in zip(names_list, links, photos, list_price):
            # print(n, l, f, p)
            # with conn.cursor() as cursor:
            #     conn.autocommit = True

            db.session.add(Cars(n, l, f, p))
            db.session.commit()

            try:
                line = '{}{}{}{}{}'.format(n, '\t', l, '\t', f, '\t', str(p))
                myfile.write(line+'\n')
            except:
                pass
        # cur.close()
        # conn.close()
                # chunk = line.encode('utf-16')
                # myfile.write(chunk.decode('cp1251', 'replace')+'\n')
    file_name = ("olx" + ".csv")
    record_to_db(container, file_name)
parser()

#-----------------------------------------------

# doc = lxml.document_fromstring(request)
# #h = doc.xpath('//h1')[0].text
# wrappers = doc.xpath('//*[@class="offer-wrapper"]')
# for wrapper in wrappers:
#     el = wrapper.xpath('/table/tbody/tr[1]/td[2]/div/h3/a/strong')




    # ccc = container_text.find('p', attrs={ "class" : "price"})
    # print(ccc.text)
# for texts in container_text:
#     print(texts.text)



# request1 = requests.get('https://www.olx.ua/obyavlenie/nissan-leaf-2014-elektromobil-IDCanVp.html#6b9e93d28d', headers=HEADERS).content
# soup1 = BeautifulSoup(request1, 'lxml')
# container_text = soup1.find("div", attrs={ "class" : "clr lheight20 large"})
# print(container_text.text)

# l= (container_text.text).split('/n')
# print(l)
#container_text = soup.select('div:clr lheight20 large')
# print(container_text)
# for i in container_text:
#     print(i.content)

  #  print(i.attrs["src"])
#price = soup.select('span.current-price-container')


#request = requests.get('https://www.pinterest.com/pin/735986764087357271/', headers=HEADERS).content
#!!!els = doc.xpath('//*[@id="body-container"]/div[3]/div/div[1]/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/div/h3/a/strong')[0].text
#els = doc.xpath("//div[@id='__PWS_ROOT__']//div[@class='gridCentered']/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[1]/a/div/div[1]/div/div/div/div/div/img")
#els = doc.xpath("//div[@id='__PWS_ROOT__']").text
#//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/div/div[1]  /div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[1]/a/div/div[1]/div/div/div/div/div/img