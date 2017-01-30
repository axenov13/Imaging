import serial
import time
import Tkinter
import SimpleScan
import ConvoScan
import ImageMaster
import FileManager


width = 700
height = 500
brick = 100
scantype = "convo"
name = "duct tape lines on glass"

ser = serial.Serial(port='COM4', baudrate=250000, timeout=10)
time.sleep(0.5)
ser.flush()
root = Tkinter.Tk()
root.bind('<Escape>', lambda e: root.destroy())
canv = Tkinter.Canvas(root, width=width, height=height, bg="black")
canv.pack()
canv.update()
FM = FileManager.FileManager()

global _s
_s = 0
def start(self):
    global _s
    _s = 1
root.bind('<s>', start)
while _s == 0:
    time.sleep(0.2)
    canv.update()

result = None
image_path = None
if scantype == "simple":
    SS = SimpleScan.SimpleScan(brick)
    SS.scan_brick(ser, canv, latency=0.02)
    SS.normalize_brick(1, 99)
    result = SS.list
if scantype == "convo":
    CS = ConvoScan.ConvoScan(brick)
    CS.init_gauss_cmatrix(5)
    CS.convoscan(canv, ser, latency=0.1)
    CS.normalize_imatrix(1, 99)
    result = CS.imatrix
FM.save_matrix(result, name, scantype, brick)
im = ImageMaster.create_image(result, brick)
FM.save_image(im, name, scantype, brick)
imtk = ImageMaster.create_tk_image(result, brick)
canv.create_image((canv.winfo_width()/2, canv.winfo_height()/2), image=imtk)
canv.update()

time.clock()
while True:
    if time.clock() > 1000:
        break
    time.sleep(0.02)
    canv.update()
exit(0)
Tkinter.mainloop()
