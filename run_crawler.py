import signal
import threading


from libs.crawler_uk import CarCrawler

if __name__ == '__main__':
    exit_event = threading.Event()

    def call_stop(*args):
        exit_event.set()

    signal.signal(signal.SIGINT, call_stop)


    sg = CarCrawler(exit_event)
    sg.run()
