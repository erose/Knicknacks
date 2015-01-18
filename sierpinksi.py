import time
from copy import copy
WorldSize = 150

class Animation:

    def __init__(self):
        self.world = [0] * WorldSize
        self.newWorld = [0] * WorldSize

    def update(self):
        for i, cell in enumerate(self.newWorld):
            self.newWorld[i] = self.ruleset[(
                                             self.world[(i - 1 + WorldSize) % WorldSize],
                                             self.world[i],
                                             self.world[(i + 1 + WorldSize) % WorldSize]
                                             )]
        self.world = copy(self.newWorld)

    def set_up(self):
        #put one black cell in the middle
        self.world[WorldSize / 2] = 1

        #the definition for rule 110
        """
        self.ruleset = {
                    (1, 1, 1) : 0,
                    (1, 1, 0) : 1,
                    (1, 0, 1) : 1,
                    (1, 0, 0) : 0,
                    (0, 1, 1) : 1,
                    (0, 1, 0) : 1,
                    (0, 0, 1) : 1,
                    (0, 0, 0) : 0
                    }
        """

        #the definition for rule 90
        self.ruleset = {
                    (1, 1, 1) : 0,
                    (1, 1, 0) : 1,
                    (1, 0, 1) : 0,
                    (1, 0, 0) : 1,
                    (0, 1, 1) : 1,
                    (0, 1, 0) : 0,
                    (0, 0, 1) : 1,
                    (0, 0, 0) : 0
                    }

    def display(self):
        print ''.join(["x" if cell else "." for cell in self.world])

if __name__ == "__main__":
    a = Animation()
    a.set_up()
    a.display()
    while True:
        time.sleep(.05)
        a.update()
        a.display()