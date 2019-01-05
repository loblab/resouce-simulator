import time
import threading
from tsdb_app import *

class WorkerThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.log = app.log

    def run(self):
        self.log.info("Worker thread start...")
        loop = self.app.args.loop
        while loop != 0 and not self.app.quit_flag:
            self.app.execute()
            self.app.report()
            self.app.sleep()
            if loop > 0:
                loop -= 1
        self.log.info("Worker thread quit.")
        return 0

class SimApp(TsdbApp):

    DEFAULT_CYCLE = 0.01
    DEFAULT_LOOP = 1000

    def main(self):
        thread = None
        self.startup()
        self.prepare()
        thread = WorkerThread(self)
        thread.start()
        self.process()
        if not thread is None:
            thread.join()
        self.cleanup()
        self.log.info("Application quit.")

    def init(self):
        self.argps.add_argument('-c', '--cycle', dest='cycle', type=float,
                default=self.DEFAULT_CYCLE,
            help="Clock cycle. default %.3f(second)" % self.DEFAULT_CYCLE)
        self.argps.add_argument('-l', '--loop', dest='loop', type=int,
                default=self.DEFAULT_LOOP,
            help="Loop count. default %d. -1 is forever" % self.DEFAULT_LOOP)
        self.objects = []

    def add_object(self, *objs):
        for obj in objs:
            self.log.info("Add object '%s'", obj.name)
            obj.log = self.log
            self.objects.append(obj)

    def sleep(self, clock=1):
        time.sleep(self.args.cycle * clock)

    def prepare(self):
        self.log.info("Prepare the resources...")

    def process(self):
        self.log.info("Main process...")

    def execute(self):
        self.log.debug("Cycle execute...")
        for obj in self.objects:
            obj.execute()

    def report(self):
        self.log.debug("Cycle status report...")
        points = []
        for obj in self.objects:
            point = {
                "measurement": "data",
                "tags": {
                    "object": obj.name,
                },
                "fields": {
                    "value": obj.value,
                },
            }
            points.append(point)
        self.tsdb.write_points(points)

