#!/usr/bin/python3
import sys
from sim_app import SimApp
from resource import *

ID = "resim"
DESC = "Resource simulator"

class App(SimApp):

    def prepare(self):
        self.log.info("Prepare the resources...")
        self.add_object(Power("Power1", 20))
        self.add_object(Power("Power2", 30))
        self.add_object(Power("Power3", 30, 10))

    def process(self):
        self.log.info("Main process...")


if __name__ == "__main__":
    app = App(ID, DESC)
    sys.exit(app.main())

