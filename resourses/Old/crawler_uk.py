import threading
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from libs.database import db_session
from libs.rabbit_wrapper import RabbitQueue
from libs.car import Cars
from settings import (DRIVER_PATH, IS_HEADLESS, NUM_WORKERS, PAGE_URL0,
                      CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME
                      )
from libs.database import DbPg
from libs.init_logger import init_logger
from libs.proxy_manager import ProxyManager
from libs.car import Cars
from libs.tasks_generator import Pages
from libs.database import db_session
from bs4 import BeautifulSoup
import requests, re, json


HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'accept' : '*/*'
}
file_name = ("uk_cars" + ".json")
full_json = {}

USE_PROXY = False


class CarCrawler:
    def __init__(self, ex_ev):
        self.log = init_logger(self.__class__.__name__)
        if USE_PROXY:
            self.proxy_gen = ProxyManager(
                self.log, ok_timeout=30, ban_timeout=1000)
        self.workers = []
        self.exit_event = ex_ev

    def run(self):
        for wnum in range(NUM_WORKERS):
            worker = threading.Thread(
                target=self.work, args=(wnum,), daemon=True
            )
            self.workers.append(worker)

        for w in self.workers:
            w.start()

        while not self.exit_event.is_set():
            count_alive = [int(w.is_alive()) for w in self.workers]

            self.log.debug(f'CarCrawler is working: {count_alive} of '
                           f'{NUM_WORKERS} is alive')
            if self.exit_event.wait(30):
                break
        for w in self.workers:
            w.join()
        self.log.info('CarCrawler exit run')


    def work(self, wnum):
        self.log.debug(f'{wnum} worker started')
        rab_connection = RabbitQueue(CRAWLER_EXCHANGE_NAME, CRAWLER_QUEUE_NAME)
        db_connection = DbPg(logger=None)
        # driver, prox = self.init_browser()
        for raw_msg in rab_connection.get_generator(self.exit_event):
            if not raw_msg:
                if self.exit_event.wait(2):
                    break
                continue

            msg = raw_msg.json()
            print(msg)

            if 'url' not in msg:
                self.log.warning(f'{wnum}: bad task: {msg}')
                raw_msg.ack()
                continue
            print()
            if msg['num'] == 0:
                msg['url'] = PAGE_URL0
                # msg['url'] = msg['url'].split('?')[0]
                print("0",msg)

            try:
                # driver.get(msg['url'])
                request = requests.get(msg['url'], headers=HEADERS).content
                soup = BeautifulSoup(request, 'html.parser')
                # container = soup.select("li.search-page__result")

                self.log.debug(msg['url'])
                # self.log.debug(driver.current_url)
                time.sleep(1)

                names_list = []
                container_names = soup.select('div.information-container h2 a')
                for name in container_names:
                    str_name = name.text
                    #name = str_name.strip()
                    print(str_name)
                    names_list.append(str_name)

                links = []
                container_links = soup.select('div.information-container h2 a')
                for i in container_links:
                    ii = i['href'].split("&")[0]
                    # ii = i['href']
                    full_link = ("https://www.autotrader.co.uk" + ii)
                    link = full_link.split('?')[0]
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

                for n, l, f, p in zip(names_list, links, photos, list_price):

                    db_session.add(Cars(n, l, f, p))
                    db_session.commit()

                    data = '{}{}{}{}{}'.format(n, '\t', l, '\t', f, '\t',str(p))
                                                                    # parse with selenium
                                                                    # rows = driver.find_elements_by_css_selector("tr")
                                                                    # if not rows:
                                                                    #     self.log.debug(f'{wnum}: not rows in table')
                                                                    #     raw_msg.nack(requeue=True)
                                                                    #     break
                                                                    #
                                                                    # for row in rows:
                                                                    #     cells = row.find_elements_by_css_selector("td")
                                                                    #     if not cells:
                                                                    #         continue
                                                                    #
                                                                    #     data = {
                                                                    #         'img_url': cells[0].find_element_by_css_selector(
                                                                    #             'img').get_attribute('src'),
                                                                    #         'country': cells[1].find_element_by_css_selector(
                                                                    #             'span').get_attribute('title'),
                                                                    #         'vessel_name': cells[1].text.split('\n')[0],
                                                                    #         'vessel_type': cells[1].text.split('\n')[1],
                                                                    #         'year': cells[2].text,
                                                                    #         'gt': cells[3].text,
                                                                    #         'dwt': cells[4].text,
                                                                    #         'sz': cells[5].text
                                                                    #     }
                                                                    #     vlength, vwidth = [int(v.strip()) for v in data['sz'].split('/')]
                    self.log.debug(data)


                                                    #     db_connection.insert_ship(car)
                                                    # db_connection.exec_query(f'''
                                                    #     INSERT INTO pages (page_num)
                                                    #     VALUES({msg['num']})
                                                    # ''')
                db_session.add(Pages(msg['num']))
                db_session.commit()
                raw_msg.ack()
            except Exception as e0:
                self.log.exception()(f'{wnum}: get page error: {e0}')##self.log.error
                raw_msg.nack(requeue=True)
                prox = None
                if USE_PROXY:
                    self.proxy_gen.back_proxy(prox, str(e0))
                # driver.close()
                # driver, prox = self.init_browser()
            time.sleep(random.randrange(1, 5))

        rab_connection.close()
        # db_connection.close()
        self.log.info(f'{wnum}: worker exit')











    # def init_browser(self):
    #     prox = None
    #     driver = None
    #     while not self.exit_event.is_set():
    #         if USE_PROXY:
    #             prox = self.proxy_gen.next_proxy()
    #
    #             self.log.debug(f'try proxy: {prox}')
    #             try:
    #                 status = prox.check_proxy()
    #             except Exception as e0:
    #                 self.log.debug(f'bad proxy: {prox}: {e0}')
    #                 self.proxy_gen.back_proxy(prox, str(e0))
    #                 continue
    #             self.log.debug(f'proxy: {prox}: {status}: OK')
    #
    #         # setup chrome options
    #         # https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/
    #         chrome_options = Options()
    #         chrome_options.binary_location = "/bin/chromedriver"
    #         chrome_options.add_argument("--incognito")
    #         chrome_options.add_argument("--disable-dev-shm-usage")
    #         chrome_options.add_argument("--disable-gpu")
    #         chrome_options.add_argument("--no-sandbox")
    #
    #         # chrome_options.add_argument("--user-data-dir="/path/to/profile")
    #         chrome_options.add_argument("--window-size=1920,1080")
    #         chrome_options = webdriver.ChromeOptions()
    #         if IS_HEADLESS:
    #             chrome_options.add_argument('headless')
    #         chrome_options.add_argument('--no-sandbox')
    #
    #         if USE_PROXY:
    #             proxy_str = '--proxy-server=https://{0}:{1}'.format(
    #                 prox.ip, str(prox.port))
    #             chrome_options.add_argument(proxy_str)
    #
    #         driver = webdriver.Chrome(chrome_options=chrome_options,
    #                                   executable_path=DRIVER_PATH)
    #         driver.implicitly_wait(10)
    #         break
    #
    #     return driver, prox
