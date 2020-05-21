from sqlalchemy import Column, Integer
from libs.database import Base, init_db, db_session
from libs.init_logger import init_logger
from libs.rabbit_wrapper import RabbitQueue
from libs.database import DbPg
from settings import (CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME,
                      PAGE_URL, MAX_PAGES, MAX_QUEUE_SIZE)#


class CarGenerator:
    def __init__(self, exit_event):
        self.exit_event = exit_event
        self.log = init_logger('cars_url_generator')
        self.was_pages = {}
        self.db = DbPg(self.log)
        self.rqueue = RabbitQueue(CRAWLER_EXCHANGE_NAME, CRAWLER_QUEUE_NAME)
        self.wait_queue()
        self.init_progress_table()
        self.get_ready_tasks()


    def wait_queue(self):
        while self.rqueue.count() > 0:
            self.log.info('Generator waiting ...')
            if self.exit_event.wait(10):
                break


    def get_ready_tasks(self):
        for row in Pages.get_pages():
            self.was_pages[row[0]] = True
        self.log.debug(f'total ready tasks: {len(self.was_pages)}')


    def run(self):
        for i in range(MAX_PAGES):
            if self.exit_event.is_set():
                break

            if self.was_pages.get(i):
                continue

            msg = {'url': PAGE_URL.format(num=i), 'num':i}
            print('run',msg)

            self.log.debug(f'[{i}]: queue size is: {self.rqueue.count()}')
            while self.rqueue.count() > MAX_QUEUE_SIZE:
                self.log.info('Queue too big, wait')
                if self.exit_event.wait(5):
                    return

            self.rqueue.publish(msg)
        self.log.info('all tasks are generated')


    def init_progress_table(self):
        delete_Pages()
        init_db()

# run()
class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    page_num = Column(Integer)


    def __init__(self, page_num=None):
        self.page_num = page_num


    def __repr__(self):
        return '<Pages %r>' % (self.page_num)


    def get_pages():
        pages = []
        for class_instance in db_session.query(Pages).all():
            u = vars(class_instance)
            pages.append(u.get('page_num'))
        return pages


def delete_Pages():
    try:
        num_rows_deleted = db_session.query(Pages).delete()
        db_session.commit()
    except:
        db_session.rollback()

init_db()
