from PIL import Image
from PIL import ImageTk


def create_image(matrix, x_blocksize=1, y_blocksize='E'):
    if y_blocksize == 'E':
        y_blocksize = x_blocksize
    im = Image.new("L", ((x_blocksize+1)*len(matrix[0]), (y_blocksize+1)*len(matrix)), "black")
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            for k in xrange(y_blocksize):
                for l in xrange(x_blocksize):
                    im.putpixel((j*x_blocksize+l, i*y_blocksize+k), int(round(255*matrix[i][j]/100)))
    return im


def create_tk_image(matrix, x_blocksize=1, y_blocksize='E'):
    if y_blocksize == 'E':
        y_blocksize = x_blocksize
    im = create_image(matrix, x_blocksize, y_blocksize)
    imtk = ImageTk.PhotoImage(im)
    return imtk
