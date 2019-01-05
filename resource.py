import math

class Resource:

    MIN = 0.0
    AMP = 100.0

    def __init__(self, name, val=0):
        self.name = name
        self.value = self.AMP * val + self.MIN
        self.time = 0

    def execute(self):
        self.time += 1


class Function(Resource):

    def __init__(self, name, func):
        super().__init__(name)
        self.func = func

    def execute(self):
        self.time += 1
        self.value = self.func(self.time) * self.AMP + self.MIN


class Usage(Resource):

    def __init__(self, name, base=0.0):
        super().__init__(name)
        self.usage = base

    def change_usage(self, usage):
        self.usage += usage
        self.value = self.AMP * self.usage + self.MIN


class Pluse(Resource):

    def __init__(self, name, width=1):
        super().__init__(name)
        self.width = width
        self.t1 = None
        self.dur = None

    def trigger(self):
        self.t1 = self.time
        self.dur = self.width

    def execute(self):
        self.time += 1
        if self.dur is None:
            return
        if self.dur > 0:
            self.value = self.MIN + self.AMP
            self.dur -= 1
        else:
            self.value = self.MIN
            self.dur = None

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

