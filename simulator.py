#!/usr/bin/python3
import sys
import time
import math
from sim_app import SimApp
from resource import *

ID = "resim"
DESC = "Resource simulator"

class Camera(Resource):

    IDLE = 0
    EXPOSING = 1
    EXPOSED = 2
    TRANSFERRING = 3
    NW_USAGE = 0.99

    def __init__(self, name, exptime=30, txwait=0, txtime=100):
        super().__init__(name)
        self.exptime = exptime
        self.txwait = txwait
        self.txtime = txtime
        self.status = self.IDLE

    def set_network(self, nic):
        self.nic = nic

    def set_lights(self, *lights):
        self.lights = list(lights)

    def trigger(self):
        if self.status != self.IDLE:
            self.log.warning("Camera %s: wrong status (%d) to trigger; wait: %d",
                    self.name, self.status, self.wait)
            return
        self.wait = self.exptime
        self.status = self.EXPOSING
        self.log.debug("Camera %s: start exposing; next wait: %d", self.name, self.wait)

    def execute(self):
        self.time += 1
        if self.status == self.IDLE:
            return
        if self.status == self.EXPOSING:
            if self.wait > 0:
                self.wait -= 1
                s = 0
                for lt in self.lights:
                    s += lt.value
                r = int(s + 0.5)
                if r > 1:
                    s /= r
                self.value = s
            else:
                self.value = 0
                self.wait = self.txwait
                self.status = self.EXPOSED
                self.log.debug("Camera %s: exposed; next wait: %d", self.name, self.wait)
        if self.status == self.EXPOSED:
            if self.wait > 0:
                self.wait -= 1
            else:
                self.wait = self.txtime
                self.status = self.TRANSFERRING
                self.nic.use(self.NW_USAGE)
                self.log.debug("Camera %s: start transferring; next wait: %d", self.name, self.wait)
        if self.status == self.TRANSFERRING:
            if self.wait > 0:
                self.wait -= 1
            else:
                self.status = self.IDLE
                self.nic.use(-self.NW_USAGE)
                self.log.debug("Camera %s: transferring completed", self.name)


class App(SimApp):

    def test(self):
        wave1 = lambda t: math.sin(2 * math.pi * t / 100) * 0.5 + 0.5
        wave2 = lambda t: math.sin(2 * math.pi * (t - 40) / 80) * 0.5 + 0.5
        wave3 = lambda t: 0 if int(t / 100) % 2 == 0 else 1
        t1 = Function("T1", wave1)
        t2 = Function("T2", wave2)
        t3 = Function("T3", wave3)
        self.add_object(t1, t2, t3)

    def prepare(self):
        self.log.info("Prepare the resources...")
        #self.test()

        sync = Pluse("SYN", 5)
        self.add_object(sync)
        self.sync = sync

        nic1 = Resource("NIC1")
        nic2 = Resource("NIC2")
        nic3 = Resource("NIC3")
        nic4 = Resource("NIC4")
        nic0 = Resource("NIC0")
        self.add_object(nic1, nic2, nic3, nic4, nic0)
        self.nic1 = nic1
        self.nic2 = nic2

        ltbg = Resource("BG", 0.1)
        ltX1 = DelayChange("X1", 30, 30, 10, 50)
        ltX2 = DelayChange("X2", 30, 30, 10, 50)
        ltX3 = DelayChange("X3", 30, 30, 10, 50)
        ltX4 = DelayChange("X4", 30, 30, 10, 50)
        ltY1234 = DelayChange("Y1234", 30, 30, 10, 50)
        ltY5 = DelayChange("Y5", 30, 30, 10, 50)

        self.add_object(ltbg, ltX1, ltX2, ltX3, ltX4, ltY1234, ltY5)
        self.ltX1 = ltX1
        self.ltX2 = ltX2
        self.ltX3 = ltX3
        self.ltX4 = ltX4
        self.ltY1234 = ltY1234
        self.ltY5 = ltY5

        camA = Camera("A", 30, 90)
        camB = Camera("B", 30, 90)
        camC = Camera("C")
        camD = Camera("D")
        camE = Camera("E", 30, 120)
        camF = Camera("F", 30, 120)
        camG = Camera("G")
        camH = Camera("H")
        camK = Camera("K")
        camM = Camera("M")
        camN = Camera("N")

        camG.set_network(nic0)
        camH.set_network(nic1)
        camA.set_network(nic1)
        camK.set_network(nic2)
        camB.set_network(nic2)
        camM.set_network(nic3)
        camC.set_network(nic3)
        camE.set_network(nic3)
        camN.set_network(nic4)
        camD.set_network(nic4)
        camF.set_network(nic4)

        camA.set_lights(ltbg, ltX1, ltX4)
        camB.set_lights(ltbg, ltX3, ltY1234, ltY5)
        camC.set_lights(ltbg, ltX3, ltY1234, ltY5)
        camD.set_lights(ltbg, ltX3, ltY1234, ltY5)
        camE.set_lights(ltbg, ltX3, ltY1234, ltY5)
        camF.set_lights(ltbg, ltX3, ltY1234, ltY5)
        camG.set_lights(ltbg, ltX2)
        camH.set_lights(ltbg, ltX2)
        camK.set_lights(ltbg, ltX2)
        camM.set_lights(ltbg, ltX2)
        camN.set_lights(ltbg, ltX2)

        self.add_object(camA, camB, camC, camD, camE, camF, camG, camH, camK, camM, camN)
        self.camA = camA
        self.camB = camB
        self.camC = camC
        self.camD = camD
        self.camE = camE
        self.camF = camF
        self.camG = camG
        self.camH = camH
        self.camK = camK
        self.camM = camM
        self.camN = camN

        self.set_view(
            'SYN',
            'X4', 'X1', 'A',
            'X3', 'Y1234', 'Y5', 'B', 'F',
            'NIC1', 'NIC2', 'NIC3', 'NIC4', 'NIC0'
            )

    def till(self, tick):
        t2 = self.args.cycle * tick + self.t1
        wait = t2 - time.time()
        if wait > 0:
            time.sleep(wait)

    def process(self):
        self.log.info("Main process...")

        self.ltX2.on()
        self.ltX3.on()
        self.ltX4.on()
        self.wait(70)

        while not self.quit_flag:
            self.t1 = time.time()
            self.sync.trigger()

            self.camG.trigger()
            self.camH.trigger()
            self.camK.trigger()
            self.camM.trigger()
            self.camN.trigger()

            self.till(20)
            self.camA.trigger()
            self.camB.trigger()

            self.till(50)
            self.ltX1.on()
            self.ltX3.off()
            self.ltX4.off()
            self.ltY1234.on()
            self.ltY5.on()

            self.till(125)
            self.camC.trigger()
            self.camD.trigger()
            self.camE.trigger()
            self.camF.trigger()

            self.till(165)
            self.ltY1234.off()

            self.till(250)
            self.camA.trigger()
            self.camB.trigger()

            self.till(290)
            self.ltX1.off()
            self.ltX3.on()
            self.ltX4.on()
            self.ltY5.off()

            self.till(500)


if __name__ == "__main__":
    app = App(ID, DESC)
    sys.exit(app.main())

