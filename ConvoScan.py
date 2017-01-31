from serial import Serial
import time
from Tkinter import *
from math import exp
from PIL import Image
from PIL import ImageTk
from __builtin__ import round
import numpy as np


def gauss(r, sigma):
    return 15 * exp(-float(r*r)/float(sigma * sigma))


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
        width = 0
        while round(gauss(width, sigma1)) > 0:
            width += 1
        height = 0
        while round(gauss(height, sigma2)) > 0:
            height += 1
        width += 1
        height += 1
        for i in range(2*height):
            self.cmatrix.append([])
            for j in range(2*width):
                self.cmatrix[i].append(round(gauss(i - height, sigma1)) * round(gauss(j - width, sigma2)))
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
        # cmatrix inizialization
        cmatrix = []

        # H COLUMN INIZIALIZATION
        convcolumn = []
        for i in xrange(len(hmatrix)):
            for j in xrange(len(hmatrix[i])):
                convcolumn.append(hmatrix[i][j])
            for k in xrange(len(cmatrix[0]) - 1):
                convcolumn.append(0.)
        for i in xrange((len(cmatrix) - 1) * (len(hmatrix[0]) + len(cmatrix[0]) - 1)):
            convcolumn.append(0.)

        # END OF H COLUMN INIZIALIZATION

        # GMATRIX INIZIALIZATION
        firstrow = []
        for i in xrange(len(cmatrix)):
            for j in xrange(len(cmatrix[j])):
                    firstrow.append(cmatrix[i][j])
            for l in xrange(len(hmatrix[0]) - 1):
                firstrow.append(0.)
        l = len(firstrow)
        for j in xrange(len(convcolumn) - l):
            firstrow.append(0.)

        gmatrix = []
        k = 0
        for i in xrange(len(convcolumn)):
        #    for j in xrange(len(hmatrix[0])):
                gmatrix.append(list(firstrow))
                firstrow.reverse()
                firstrow.pop(0)
                firstrow.append(0.)
                firstrow.reverse()
                k += 1
            #for j in xrange(len(cmatrix[0]) - 1):
            #    firstrow.reverse()
            #    firstrow.pop(0)
            #    firstrow.append(0.)
            #    firstrow.reverse()
            #    marker = (len(convcolumn) - 1) * [0.]
            #    marker.insert(k, 1.)
            #    k += 1
             #   gmatrix.append(marker)
        #for i in xrange((len(cmatrix) - 1) * (len(hmatrix[0]) + len(cmatrix[0]) - 1)):
        #    marker = (len(convcolumn) - 1) * [0.]
        #   marker.insert(k, 1.)
        #    k += 1
        #    gmatrix.append(marker)

        # END OF GMATRIX INIZIALIZATION

        # SOLVING
        f = np.linalg.solve(gmatrix, convcolumn)
        f = np.array(f).reshape((len(hmatrix) + len(cmatrix) - 1, len(hmatrix[0]) + len(cmatrix[0]) - 1))

        # END

        self.imatrix = f
        return self.imatrix

    def create_cmatrix_image(self):
        self.cmatrix_image = Image.new("L", (len(self.cmatrix[0])*self.x_blocksize,
                                             len(self.cmatrix)*self.y_blocksize), "black")
        for i in xrange(len(self.cmatrix)):
            for j in xrange(len(self.cmatrix[0])):
                for k in xrange(self.x_blocksize):
                    for l in xrange(self.y_blocksize):
                        self.cmatrix_image.putpixel((j+k, i+l), int(self.cmatrix[i][j]))
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
            line = ser.readline()
            if not line.strip():
                i -= 1
                continue
            summ += int(line)
        return float(summ) / iterations

    def convoscan(self, canv, ser, latency=0.05):
        i = self.create_cmatrix_image()
        itk = ImageTk.PhotoImage(i)
        img = canv.create_image((0, 0), image=itk)
        canv.update()
        time.sleep(latency)
        self.convolution = []
        for i in xrange(canv.winfo_height() / self.y_blocksize + 1):
            conv1 = []
            for j in xrange(canv.winfo_width() / self.x_blocksize + 1):
                conv1.append(self.get_signal(ser))
                canv.move(img, self.x_blocksize, 0)
                canv.update()
                time.sleep(latency)
            self.convolution.append(conv1)
            canv.move(img, -(canv.winfo_width() / self.x_blocksize + 1) * self.x_blocksize, self.y_blocksize)
            print i, j
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
        self.imatrix = np.around(k*self.imatrix + b)
        return self.imatrix

