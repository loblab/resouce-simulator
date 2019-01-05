import time
import threading
from tsdb_app import *

class WorkerThread(threading.Thread):
    def __init__(self, app):
        super(WorkerThread, self).__init__()
        self.app = app
        self.log = app.log

    def run(self):
        self.log.info("Worker thread start...")
        loop = self.app.args.loop
        while loop != 0 and not self.app.quit_flag:
            self.app.execute()
            self.app.report()
            time.sleep(self.app.args.cycle)
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

    def process(self):
        self.log.info("Main process...")

    def execute(self):
        self.log.debug("Cycle execute...")

    def report(self):
        self.log.debug("Cycle status report...")

