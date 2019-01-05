import math

class Resource:

    MIN = 0.0
    AMP = 100.0

    def __init__(self, name):
        self.name = name
        self.value = self.MIN
        self.time = 0

    def execute(self):
        self.time += 1


class Usage(Resource):

    def __init__(self, name, base=0.0):
        super().__init__(name)
        self.usage = base

    def change_usage(self, usage):
        self.usage += usage
        self.value = self.AMP * self.usage + self.MIN


class DelayChange(Resource):

    def __init__(self, name, delay_up=0, leading=0, delay_down=0, trailing=0):
        super().__init__(name)
        self.leading = leading
        self.trailing = trailing
        self.delay_up = delay_up
        self.delay_down = delay_down
        # for changing status
        self.delay = None
        self.t1 = None
        self.v1 = None
        self.period = 0

    def change(self, value):
        self.v1 = self.value
        self.v2 = value
        if value >= self.value:
            self.delay = self.delay_up
            self.period = (self.v2 - self.v1) / self.AMP * self.leading
        else:
            self.delay = self.delay_down
            self.period = (self.v1 - self.v2) / self.AMP * self.trailing
        if self.period == 0:
            self.period = 1

    def on(self):
        self.change(self.MIN + self.AMP)

    def off(self):
        self.change(self.MIN)

    def execute(self):
        self.time += 1
        if self.delay is None:
            return
        if self.delay > 0:
            self.delay -= 1
            if self.delay <= 0:
                self.delay = 0
                self.t1 = self.time
        else:
            r = (self.time - self.t1) / self.period
            if r >= 1:
                self.value = self.v2
                self.t1 = None
                self.delay = None
            else:
                self.value = (self.v2 - self.v1) * r + self.v1

class Power(Resource):

    def __init__(self, name, cycle=20, phase=0):
        super().__init__(name)
        self.cycle = cycle
        self.time += phase

    def execute(self):
        self.value = math.sin(2 * math.pi * self.time / self.cycle) * self.AMP + self.MIN
        self.time += 1

