

import threading
import signal

from libs.tasks_generator import CarGenerator

if __name__ == '__main__':
    exit_event = threading.Event()

    def call_stop(*args):
        exit_event.set()

    signal.signal(signal.SIGINT, call_stop)

    #sg = CarGenerator(exit_event)
    sg = CarGenerator()
    sg.run()
