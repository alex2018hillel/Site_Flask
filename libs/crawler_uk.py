import threading, random, time, requests, re
from libs.rabbit_wrapper import RabbitQueue
from settings import (NUM_WORKERS, PAGE_URL0,
                      CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME
                      )
from libs.database import DbPg
from libs.init_logger import init_logger
from libs.proxy_manager import ProxyManager
from libs.car import Cars
from libs.tasks_generator import Pages
from libs.database import db_session
from bs4 import BeautifulSoup


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
                print("0",msg)

            try:
                request = requests.get(msg['url'], headers=HEADERS).content
                soup = BeautifulSoup(request, 'html.parser')

                self.log.debug(msg['url'])
                time.sleep(1)

                names_list = []
                container_names = soup.select('div.information-container h2 a')
                for name in container_names:
                    str_name = name.text
                    print(str_name)
                    names_list.append(str_name)

                links = []
                container_links = soup.select('div.information-container h2 a')
                for i in container_links:
                    ii = i['href'].split("&")[0]
                    full_link = ("https://www.autotrader.co.uk" + ii)
                    link = full_link.split('?')[0]
                    links.append(link)

                photos = []
                container_photo = soup.select('figure.listing-main-image a img')
                for link_photo in container_photo:
                    photos.append(link_photo['src'])

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
                    self.log.debug(data)

                db_session.add(Pages(msg['num']))
                db_session.commit()
                raw_msg.ack()
            except Exception as e0:
                self.log.exception()(f'{wnum}: get page error: {e0}')##self.log.error
                raw_msg.nack(requeue=True)
                prox = None
                if USE_PROXY:
                    self.proxy_gen.back_proxy(prox, str(e0))

            time.sleep(random.randrange(1, 5))

        rab_connection.close()
        self.log.info(f'{wnum}: worker exit')


