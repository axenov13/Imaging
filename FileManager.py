from PIL import Image
from PIL import ImageTk
import datetime as dt
import os.path
import time


class FileManager:
    def __init__(self):
        self.date = dt.datetime.now().date()
        self.directory = "C:\Users\Aksenov_Kalacheva\PycharmProjects\Imaging\Files\\" + str(self.date)

    def save_matrix(self, matrix, name="IMAGE", scantype="undefined", x_blocksize=1, y_blocksize='E'):
        if y_blocksize == 'E':
            y_blocksize = x_blocksize
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        filename = "{0}\{1}_{2} xbs= {3} ybs= {4} #1.txt".format(self.directory, name, scantype, str(x_blocksize),
                                                                 str(y_blocksize))
        i = 1
        file_obj = None
        while i < 10000:
            if os.path.isfile(filename):
                i += 1
                filename = filename[:len(filename)-5]
                filename += str(i)
                filename += '.txt'
            else:
                file_obj = open(filename, 'w')
                break
            if i > 9000:
                print "YOU ARE INSANE"
                time.sleep(30)
        for i in xrange(len(matrix)):
            for j in xrange(len(matrix[0])):
                file_obj.write(str(matrix[i][j])+'\t')
            file_obj.write('\n')
        file_obj.close()
        return filename

    def save_image(self, image, name="IMAGE", scantype="undefined", x_blocksize=1, y_blocksize='E'):
        if y_blocksize == 'E':
            y_blocksize = x_blocksize
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        filename = '{0}\{1}_{2} xbs= {3} ybs= {4} #1.bmp'.format(self.directory, name, scantype, str(x_blocksize),
                                                                 str(y_blocksize))
        i = 1
        while i < 10000:
            if os.path.isfile(filename):
                i += 1
                filename = filename[:len(filename) - 5]
                filename += str(i)
                filename += '.bmp'
            else:
                image.save(filename)
                break
            if i > 9000:
                print "YOU ARE INSANE"
                time.sleep(30)
        return filename

