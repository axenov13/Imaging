from PIL import Image
from PIL import ImageTk

def create_image(matrix, blocksize=1):
    im = Image.new("L", (len(matrix), len(matrix[0]), "black"))
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            for k in xrange(blocksize):
                im.putpixel((i + k * blocksize, j + k * blocksize), int(matrix[i][j]))
    return im


def create_tk_image(matrix, blocksize=1):
    im = create_image(matrix, blocksize)
    imtk = ImageTk.PhotoImage(im)
    return imtk
