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

# params for db (sqlite)
DB_NAME = os.environ.get(
    'DATABASE_URL',
    f'sqlite:///{os.path.join(os.getcwd(), "db", "ships.sqlite3")}'
)
DB_URL = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES

# params for rabbit queue

# params for proxy
PROXY_FILE_PATH ='/resourses/proxies.txt'
# configs for crawler