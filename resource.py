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

class Power(Resource):

    def __init__(self, name, cycle=20, phase=0):
        super().__init__(name)
        self.cycle = cycle
        self.time += phase

    def execute(self):
        self.value = math.sin(2 * math.pi * self.time / self.cycle) * self.AMP + self.MIN
        self.time += 1

