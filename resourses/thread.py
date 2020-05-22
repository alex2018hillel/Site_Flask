from threading import Thread
import rabbitpy
from settings import RABITMQ_URL


class RabbitQueue:

    def __init__(self, exchange_name, queue_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = queue_name

        self.connection = rabbitpy.Connection(RABITMQ_URL)
        self.channel = self.connection.channel()

        self.exchange = rabbitpy.Exchange(
            self.channel, self.exchange_name, durable=True)
        self.exchange.declare()

        self.queue = rabbitpy.Queue(
            self.channel, self.queue_name, durable = True)
        self.queue.declare()

        self.queue.bind(self.exchange_name, routing_key=self.routing_key)

    def publish(self, msg:dict):
        m = rabbitpy.Message(self.channel, msg)
        m.publish(self.exchange_name, routing_key=self.routing_key)

    def consume(self, threads=2):
        for msg in self.queue.consume():
            data = msg.json()
            if not data:
                msg.ack()
                print('break')
                break
            # print(data)

    def count(self):
        return  len(self.queue)

    def close(self):
        self.channel.close()
        self.connection.close()


rq = RabbitQueue('test5_exchange', 'test5_queue_name')

def publish_thread(num):
    if rq.count() == 0:
        for i in range(50):
            rq.publish({'url': f'https://{i}'})
    rq.publish({})

def consume_thread():
    rq.consume()

thread1 = Thread(target=publish_thread, args=( 2000,))
thread2 = Thread(target=consume_thread)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

rq.close()