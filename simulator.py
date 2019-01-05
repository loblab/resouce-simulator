#!/usr/bin/python3
import sys
from sim_app import SimApp
from resource import *

ID = "resim"
DESC = "Resource simulator"

class App(SimApp):

    def prepare_demo(self):
        self.log.info("Prepare the demo resources...")
        self.add_object(Power("Power1", 80))
        self.add_object(Power("Power2", 100))
        self.add_object(Power("Power3", 100, 40))

    def prepare(self):
        self.log.info("Prepare the resources...")
        sync = Pluse("SYN")
        self.add_object(sync)
        self.sync = sync
        nic1 = Usage("NIC1", 0.05)
        nic2 = Usage("NIC2", 0.10)
        nic3 = Usage("NIC3", 0.15)
        nic4 = Usage("NIC4", 0.20)
        nic5 = Usage("NIC5", 0.25)
        self.add_object(nic1, nic2, nic3, nic4, nic5)
        self.nic1 = nic1
        self.nic2 = nic2
        ltx1 = DelayChange("X1", 30, 30, 10, 50)
        ltx2 = DelayChange("X2", 30, 30, 10, 50)
        self.add_object(ltx1, ltx2)
        self.ltx1 = ltx1
        self.ltx2 = ltx2

    def process(self):
        self.log.info("Main process...")
        while not self.quit_flag:
            self.ltx1.on()
            self.sleep(5)
            self.ltx2.on()
            self.sleep(60)
            self.sync.trigger()
            self.nic1.change_usage(0.7)
            self.sleep(20)
            self.ltx1.off()
            self.sleep(5)
            self.ltx2.off()
            self.nic2.change_usage(0.7)
            self.sleep(40)
            self.nic2.change_usage(-0.7)
            self.sleep(10)
            self.nic1.change_usage(-0.7)
            self.sleep(10)


if __name__ == "__main__":
    app = App(ID, DESC)
    sys.exit(app.main())

