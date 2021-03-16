import lithops.multiprocessing as mp

import actors.director as director


class Director(object):

    def __init__(self):
        # self.actors = {}
        # self.queue = mp.Queue()
        self.manager = mp.Manager()
        self.actors = self.manager.dict()  # TODO: self.manager.__dict__

    def new_actor(self, actor_type, weak_ref, args, kwargs):
        actor_queue = mp.Queue()
        self.actors[weak_ref._thtr_actor_key] = actor_queue
        event = self.manager.Event()  # TODO: self.manager?.Event()
        actor_ps = mp.Process(target=director.actor_process,
                              args=(actor_type, weak_ref,
                                    actor_queue, self.actors, event,
                                    args, kwargs))
        actor_ps.start()
        # we need to wait for the child to be working,
        # otherwise, the queue loses events
        event.wait()
        return actor_ps

    def run(self) -> None:
        # def p():
        #     while self.running:
        #         try:
        #             m = self.queue.get(timeout=1)
        #             dest = m[0]
        #             msg = m[1]
        #             self.actors[dest].put(msg)
        #         except Empty:
        #             pass
        #
        self.running = True
        # self.t = Thread(target=p)
        # self.t.start()

    def stop(self) -> None:
        # stop all actors
        for actor in self.actors.keys():
            self.msg2(actor, 'pls stop')
        self.running = False
        # self.t.join()

    def msg2(self, actor_key, msg):
        self.actors[actor_key].put(msg)
