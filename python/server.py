execfile("core.py")
import serial
from enum import Enum
import time

class States(Enum):
    MOVING = 0
    STATIONARY = 1
    SITTING = 2

class Direction(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    SIDEWAYSL = 3
    SIDEWAYSR = 4

class Bench:
    def __init__(self, positions, counts = [], values = []):
        self.positions = positions
        self.state = States.STATIONARY
        self.direction = Direction.STOP
        self.fPressureVal = 0
        self.fPThresh = 50

        self.bPressureVal = 0
        self.bPThresh = 50
        # self.power = 255

        self.pos = self.positions[0]
        self.posIdx = 0

        self.nextPos = self.positions[0]
        self.nextPosIdx = 0

        self.ucb = UCB1(counts, values)
        self.ucb.initialize(len(self.positions))

        self.startTime = time.mktime(time.localtime())
        self.startSittingTime = time.mktime(time.localtime())

    def checkSitting(self):
        return self.fPressureVal > self.fPThresh or self.bPressureVal > self.bPThresh

    def beginCounting(self):
        self.startTime = time.mktime(time.localtime())

    def beginSittingCounting(self):
        self.startSittingTime = time.mktime(time.localtime())

    def stopCounting(self):
        endTime =  time.mktime(time.localtime())
        st = endTime - self.startTime
        sst = endTime - self.startSittingTime

        reward = float(sst)/float(st)
        return reward

    def addPosition(self, pos):
        self.positions.append(pos)

        tempCounts = list(self.ucb.counts)
        tempValues = list(self.ucb.values)

        tempCounts.append(0)
        tempValues.append(0.0)

        self.ucb = UCB1(tempCounts, tempValues)
        return len(self.positions)-1

    def printStatus(self):
        now = time.mktime(time.localtime())
        out = ""
        out += "State: "
        if self.state == States.MOVING:
            out += "MOVING\n"
            out += "Position: " + str(self.pos) + "\n"
            out += "Next Position: " + str(self.nextPos) + "\n"
            out += "Direction: "
            if self.direction == Direction.FORWARD:
                out += "FORWARD"
            elif self.direction == Direction.BACKWARD:
                out += "BACKWARD"

            out += "\n"

        elif self.state == States.STATIONARY:
            out += "STATIONARY\n"
            out += "Position: " + str(self.pos) + "\n"
            tmp = now - self.startTime
            out += "Stationary Time: " + str(tmp)

        elif self.state == States.SITTING:
            out += "SITTING\n"
            out += "Position: " + str(self.pos) + "\n"
            tmp = now - self.startTime
            out += "Stationary Time: " + str(tmp) + "\n"
            tmp = now - self.startSittingTime
            out += "Seated Time:" + str(tmp) + "\n"

        out += "\n"
        print out

    def serialMessage(self):
        if self.direction == Direction.STOP:
            return "0,0"
        elif self.direction == Direction.FORWARD:
            return "1,255"
        elif self.direction == Direction.BACKWARD:
            return "2,255"

    def step(self, updates=None):
        if updates:
            self.fPressureVal = updates[0]
            self.bPressureVal = updates[1]

        state = self.state

        if state == States.MOVING:
            if self.checkSitting():
                self.state = States.SITTING
                self.direction = Directions.STOP
                self.beginSittingCount()
                self.beginCounting()
                self.posIdx = self.addPosition(self.pos)

            elif self.pos == self.nextPos:
                self.direction = Directions.STOP
                self.state = States.STATIONARY
                self.beginCounting()
                self.posIdx = self.nextPosIdx

            else:
                if self.direction == Directions.FORWARD:
                    self.pos = self.pos + 1
                elif self.direction == Directions.BACKWARD:
                    self.pos = self.pos - 1

        elif state == States.STATIONARY:
            if self.checkSitting():
                self.state = States.SITTING
                self.beginSittingCount()

        elif state == States.SITTING:
            if not self.checkSitting():
                reward = self.stopCounting()
                self.ucb.update(self.posIdx, reward)
                self.nextPosIdx = self.ucb.select_arm()
                self.nextPos = self.positions[self.nextPosIdx]

                if self.nextPos > self.pos:
                    self.direction = Directions.FORWARD
                elif self.nextPos < self.pos:
                    self.direction = Directions.BACKWARD

                self.state = States.MOVING

        self.printStatus()
        return self.serialMessage()

def main():
    # Arduino serial port
    # ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

    bench = Bench([0, 1, 2])

    while True:

        # updateStr = ser.readline()
        # update = updateStr.split(",")
        # update[0] = float(update[0])
        # update[1] = float(update[1])
        update = [0,0]
        msg = bench.step(update)
        # serial.write(msg)
        time.sleep(1)


if __name__ == "__main__":
    main()
