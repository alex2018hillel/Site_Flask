import os
import dotenv
dotenv.load_dotenv()

POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'auto',
    'host': 'localhost',
    'port': '5432',
}

# flask app
RANDOM_STRING = '1324'#os.getenv("RANDOM_STRING", "random string")
APP_NAME = "Suggestions Crawler"
FLASK_HOST = os.getenv("FLASK_HOST", 'localhost')
FLASK_PORT = os.getenv("FLASK_PORT", 5000)

# params for db
# DB_NAME = os.environ.get(
#     'DATABASE_URL',
#     'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
# )
DB_URL = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES


# params for rabbit queue
RABITMQ_URL = os.environ.get('RABITMQ_URL',
                             "amqp://wnuahdex:Monf5SDy2aXkPiYreQSaqe56EF2AaUJQ@squid.rmq.cloudamqp.com/wnuahdex"
                             )
PAGE_URL = "https://www.autotrader.co.uk/car-search?sort=relevance&postcode=WC2N%205DU&radius=1500&make=TESLA&page={num}"
PAGE_URL0 = "https://www.autotrader.co.uk/car-search?sort=relevance&postcode=WC2N%205DU&radius=1500&make=TESLA"
CRAWLER_QUEUE_NAME = 'car-queue'
CRAWLER_EXCHANGE_NAME = 'car-exchange'
MAX_QUEUE_SIZE = 10
MAX_PAGES = 15

# params for proxy
PROXY_FILE_PATH ='/resourses/proxies.txt'


# configs for crawler
URL = 'https://www.autotrader.co.uk/car-search?sort=relevance&postcode=WC2N%205DU&radius=1500&make=TESLA'
HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'accept' : '*/*'}


# configs for crawler
DRIVER_PATH = "bin/chromedriver"  # path to driver binary
IS_HEADLESS = True
NUM_WORKERS = 1

