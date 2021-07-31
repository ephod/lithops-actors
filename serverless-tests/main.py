# import multiprocessing as mp
import time
from queue import Empty
from threading import Thread

import lithops.multiprocessing as mp
from lithops import FunctionExecutor
from lithops.config import load_config
from lithops.utils import create_executor_id


class Counter(object):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        print(self.value)
        return self.value

    def get_value(self):
        print(self.value)
        return self.value


def actor_process(actor_type, queue, director_queue):
    instance = actor_type()
    while True:
        message = queue.get()
        print(message)
        if message == 'pls stop':
            break
        method_name, args, kwargs = message
        getattr(instance, method_name)(*args, **kwargs)


class Director(object):
    def __init__(self):
        self.actors = {}
        self.queue = mp.Queue()

    def new_actor(self, actor_type, name):
        actor_queue = mp.Queue()
        self.actors[name] = actor_queue
        fexec = FunctionExecutor()
        fexec.call_async(actor_process, (actor_type, actor_queue, self.queue))
        return fexec

    def run(self):
        def p():
            while self.running:
                try:
                    m = self.queue.get(timeout=1)
                    dest = m[0]
                    msg = m[1:]
                    self.actors[dest].put(msg)
                except Empty:
                    pass

        self.running = True
        t = Thread(target=p)
        t.start()

    def stop(self):
        self.running = False

    def msg2(self, name, msg):
        self.actors[name].put(msg)


def main():
    director = Director()
    director.run()
    count_ps = director.new_actor(Counter, 'count')

    director.msg2('count', ('increment', (), {}))
    director.msg2('count', ('get_value', (), {}))
    director.msg2('count', 'pls stop')

    count_ps.get_result()
    director.stop()


if __name__ == '__main__':
    main()
