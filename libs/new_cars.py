# import psycopg2

class New_cars:
    __slots__ = (
        'id', 'head', 'link',
        'photo', 'price'
    )

    def __init__(
            self, id, head, link, photo, price):
        self.id = id
        self.head = head
        self.link = link
        self.photo = photo
        self.price = price


    def __str__(self):
        return f'{self.head} [{self.link} - {self.price}]'

    def __repr__(self):
        return f'{self.head} [{self.link} - {self.price}]'

    def make_dict(self):
        d = {k: getattr(self, k) for k in self.__slots__}
        return d
#-------------------------------------------------------------
# POSTGRES = {
#     'user': 'postgres',
#     'pw': '123',
#     'db': 'auto',
#     'host': 'localhost',
#     'port': '5432',
# }
#-------------------------------------------------------------
# conn = psycopg2.connect(
#     database="auto",
#     user="postgres",
#     password="123",
#     host="localhost",
#     port="5432"
# )
# cur = conn.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS OLD_CARS(
#     id serial PRIMARY KEY,
#      head TEXT PRIMARY KEY NOT NULL,
#      link TEXT NOT NULL,
#      photo TEXT NOT NULL,
#      price CHAR(50))''')
#
# cur.close()
# conn.close()