from serial import Serial
import time
from Tkinter import *
from math import exp, log
from PIL import Image
from PIL import ImageTk
from __builtin__ import round
import numpy as np


def gauss(r, sigma):
    return 15 * exp(-r * r / (sigma * sigma))


class ConvoScan:
    def __init__(self, x_blocksize=1, y_blocksize='E'):
        self.cmatrix = []
        self.imatrix = []
        self.convolution = []
        self.x_blocksize = x_blocksize
        if y_blocksize == 'E':
            self.y_blocksize = x_blocksize
        else:
            self.y_blocksize = y_blocksize
        self.cmatrix_image = None
        self.cmatrix_type = None
        self.imatrix_image = None

    def _get_average_in_zone(self, x1, y1, x2, y2):
        sum = 0
        for i in range(0, x2 - x1):
            for j in range(0, y2 - y1):
                sum += self.cmatrix[i][j]
        return sum / ((x2 - x1) * (y2 - y1))

    def set_x_blocksize(self, size):
        self.x_blocksize = size
        return 0

    def set_y_blocksize(self, size):
        self.y_blocksize = size
        return 0

    def _resized_cmatrix(self):
        new = []
        if self.cmatrix_type == 'block':
            for i in range(int(len(self.cmatrix) / self.x_blocksize) + 1):
                new.append([])
                for j in range(int(self.cmatrix[0] / self.y_blocksize) + 1):
                    new[i].append(1)
        else:
            for i in range(int(len(self.cmatrix) / self.x_blocksize) + 1):
                new.append([])
                for j in range(int(len(self.cmatrix[0]) / self.y_blocksize) + 1):
                    x = self._get_average_in_zone(self.x_blocksize * i, self.y_blocksize * j,
                                                  self.x_blocksize * (i + 1), self.y_blocksize * (j + 1))
                    new[i].append(x)
        return new

    def _extand_matrix_to_square(self, matrix, size):
        while len(matrix) < size:
            matrix.append([])
        for i in range(len(matrix)):
            while len(matrix[i]) < size:
                matrix[i].append(0)
        return matrix

    def init_gauss_cmatrix(self, sigma1, sigma2='E'):
        self.cmatrix = []
        self.cmatrix_type = 'gauss'
        if sigma2 == 'E':
            sigma2 = sigma1

        width = int(round(2 * sigma1 * log(15)))
        height = int(round(2 * sigma2 * log(15)))

        i0 = int(round(width / 2))
        j0 = int(round((height / 2)))
        i = 0
        j = 0
        for i in range(width):
            self.cmatrix.append([])
            for j in range(height):
                self.cmatrix[i].append(round(gauss(float(i - i0), float(sigma1)) * gauss(float(j - j0), float(sigma2))))
        return self.cmatrix

    def init_block_cmatrix(self, x, y):
        self.cmatrix = []
        self.cmatrix_type = 'block'
        for i in range(x):
            self.cmatrix.append([])
            for j in range(y):
                self.cmatrix[i].append(1)
        return self.cmatrix

    def init_cmatrix(self, matrix):
        self.cmatrix = matrix
        self.cmatrix_type = 'manual'
        return self.cmatrix

    def init_convolution(self, convolution):
        self.convolution = convolution
        return self.convolution

    def init_imatrix(self):
        self.imatrix = []
        hmatrix = self.convolution
        cmatrix = self.cmatrix

        # H COLUMN INIZIALIZATION
        convcolumn = []
        for i in xrange(len(hmatrix)):
            for j in xrange(len(hmatrix[i])):
                convcolumn.append(hmatrix[i][j])
            for j in xrange(len(cmatrix[0]) - 1):
                convcolumn.append(0.)
        for i in xrange((len(cmatrix) - 1) * (len(hmatrix[0]) + len(cmatrix[0]) - 1)):
            convcolumn.append(0.)

        # END OF H COLUMN INIZIALIZATION

        ##### GMATRIX INIZIALIZATION
        firstrow = []
        for j in xrange(len(cmatrix)):
            for i in xrange(len(cmatrix[j])):
                firstrow.append(cmatrix[j][i])
            for i in xrange(len(hmatrix[0]) - 1):
                firstrow.append(0.)
        l = len(firstrow)
        for j in xrange(len(convcolumn) - l):
            firstrow.append(0.)

        Gmatrix = []
        k = 0
        for i in xrange(len(hmatrix)):
            for j in xrange(len(hmatrix[0])):
                Gmatrix.append(list(firstrow))
                firstrow.reverse()
                firstrow.pop(0)
                firstrow.append(0.)
                firstrow.reverse()
                k += 1
            for j in xrange(len(cmatrix[0]) - 1):
                firstrow.reverse()
                firstrow.pop(0)
                firstrow.append(0.)
                firstrow.reverse()
                marker = (len(convcolumn) - 1) * [0.]
                marker.insert(k, 1.)
                k += 1
                Gmatrix.append(marker)
        for i in xrange((len(cmatrix) - 1) * (len(hmatrix[0]) + len(cmatrix[0]) - 1)):
            marker = (len(convcolumn) - 1) * [0.]
            marker.insert(k, 1.)
            k += 1
            Gmatrix.append(marker)

        # END OF GMATRIX INIZIALIZATION

        # SOLVING
        f = np.linalg.solve(Gmatrix, convcolumn)
        f = np.array(f).reshape((len(hmatrix) + len(cmatrix) - 1, len(hmatrix[0]) + len(cmatrix[0]) - 1))

        # END

        self.imatrix = f
        return self.imatrix

    def create_cmatrix_image(self):
        self.cmatrix_image = Image.new("L", (len(self.cmatrix[0]), len(self.cmatrix)), "black")
        for i in range(len(self.cmatrix)):
            for j in range(len(self.cmatrix[0])):
                self.cmatrix_image.putpixel((j, i), int(self.cmatrix[i][j]))
                print int(self.cmatrix[i][j]),
            print
        return self.cmatrix_image

    def create_imatrix_image(self):
        self.imatrix_image = Image.new("L", (len(self.imatrix), len(self.imatrix[0])), "black")
        for i in range(len(self.imatrix)):
            for j in range(len(self.imatrix[0])):
                self.imatrix_image.putpixel((i, j), int(self.imatrix[i][j].real))
        return self.imatrix_image

    def get_imatrix_image(self):
        return self.imatrix_image

    def get_cmatrix_image(self):
        return self.cmatrix_image

    def get_cmatrix_type(self):
        return self.cmatrix_type

    def get_signal(self, ser, iterations=1):
        summ = 0
        for i in xrange(iterations):
            ser.write('w')
            time.sleep(0.005)
            line = ser.readline()
            if not line.strip():
                i -= 1
                continue
            summ += int(line)
        return float(summ) / iterations

    def convoscan(self, canv, ser, latency=0.05):
        img = canv.create_image((0, 0), image=ImageTk.PhotoImage(image=self.create_cmatrix_image()))
        canv.update()
        self.convolution = []
        for i in xrange(canv.winfo_height() / self.x_blocksize + 1):
            conv1 = []
            for j in xrange(canv.winfo_width() / self.y_blocksize + 1):
                conv1.append(self.get_signal(ser))
                canv.move(img, self.x_blocksize, 0)
                canv.update()
                time.sleep(latency)
            self.convolution.append(conv1)
            canv.move(img, -(canv.winfo_width() / self.x_blocksize + 1) * self.x_blocksize, self.y_blocksize)
            canv.update()
            time.sleep(latency)
        self.init_imatrix()

    def normalize_imatrix(self, min_norm=1, max_norm=99):
        self.imatrix = np.array(self.imatrix)
        max = np.amax(self.imatrix)
        min = np.amin(self.imatrix)
        if max - min == 0:
            max = 1
            min = 0
        k = (max_norm - min_norm)/(max - min)
        b = max_norm - k*max
        list = np.around(k*self.imatrix + b)
        return self.imatrix

