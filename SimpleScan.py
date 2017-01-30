import serial
import time
import Tkinter
import numpy as np
from __builtin__ import round


class SimpleScan:
    def __init__(self, brick, iterations=1):
        self.brick = brick
        self.iterations = iterations
        self.list = None

    def get_signal(self, ser, iterations=1):
        summ = 0
        for i in xrange(self.iterations):
            ser.write('w')
            line = ser.readline()
            if not line.strip():
                i += 1
                continue
            summ += int(line)
        return float(summ)/self.iterations

    def scan_brick(self, ser, canv, latency=0.05):
        self.list = []
        for i in xrange(canv.winfo_height()/self.brick + 1):
            list1 = []
            for j in xrange(canv.winfo_width()/self.brick + 1):
                rect = canv.create_rectangle(j*self.brick, i*self.brick, j*self.brick + self.brick,
                                                  i*self.brick + self.brick, fill="white")
                canv.update()
                time.sleep(latency)
                signal = self.get_signal(ser)
                canv.delete(rect)
                list1.append(signal)
            self.list.append(list1)
            canv.update()
        return list

    def out_brick(self, canv):
        width = self.brick
        height = self.brick
        for i in xrange(canv.winfo_height()/height + 1):
            for j in xrange(canv.winfo_width()/width + 1):
                n = self.list[i][j]
                if n < 0:
                    n = 0
                if n > 99:
                    n = 99
                col = 'gray' + str(int(round(n)))
                canv.create_rectangle(j*width, i*height, j*width + width, i*height + height, fill=col)
        canv.update()
        return 0

    def normalize_brick(self, min_norm=1, max_norm=99):
        self.list = np.array(self.list)
        max = np.amax(self.list)
        min = np.amin(self.list)
        if (max-min == 0):
            max = 1
            min = 0
        k = (max_norm - min_norm)/(max - min)
        b = max_norm - k*max
        self.list = np.around(k*self.list + b)
        return self.list

