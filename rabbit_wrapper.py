import rabbitpy
import json
#RABBIT_URL = "amqp://guest:guest@localhost:5672/%2F"
RABBIT_URL = "amqp://wnuahdex:Monf5SDy2aXkPiYreQSaqe56EF2AaUJQ@squid.rmq.cloudamqp.com/wnuahdex"

class RabbitQueue:

    def __init__(self, exchange_name, queue_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = queue_name

        self.connection = rabbitpy.Connection(RABBIT_URL)
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
        m.publish(self.exchange_name, self.routing_key)

    def consume_generator(self, threads=1):
        for msg in self.queue.consume(prefetch=threads):
            yield msg.json()
            msg.ack()

    def count(self):
        return  len(self.queue)

    def close(self):
        self.channel.close()
        self.connection.close()

rq = RabbitQueue('test_exchange', 'test_queue_name')
for i in range(100):
    rq.publish({'message':f'text {i}'})
for msg in rq.consume_generator():
    print(msg)
    break

rq.close()