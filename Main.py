import serial
import time
import Tkinter
import numpy as np
import SimpleScan
import ConvoScan
import ImageMaster
import FileManager

width = 1000
height = 800
brick = 100
scantype = "simple"
name = "lines_and_triangles"

ser = serial.Serial(port='COM4', baudrate=250000, timeout=10)
time.sleep(0.5)
ser.flush()
root = Tkinter.Tk()
canv = Tkinter.Canvas(root, width=width, height=height, bg="black")
canv.pack()
canv.update()
FM = FileManager.FileManager()

time.clock()
while(True):
    if(time.clock() > 1):
        break
    time.sleep(0.02)
    canv.update()

result = None
if type == "simple":
    SS = SimpleScan.SimpleScan(brick)
    SS.scan_brick(ser, canv, latency=0.05)
    SS.normalize_brick(1, 99)
    result = SS.list
if type == "convo":
    CS = ConvoScan.ConvoScan(brick)
    CS.init_gauss_cmatrix(50)
    CS.convoscan(canv, ser, latency=0.05)
    CS.normalize_imatrix(1, 99)
    result = CS.imatrix
FM.save_matrix(result, name, scantype, brick)
im = ImageMaster.create_image(result, brick)
FM.save_image(im, name, scantype, brick)
imtk = ImageMaster.create_tk_image(result, brick)
canv.create_image((0, 0), imtk)
canv.update()

time.clock()
while(True):
    if(time.clock() > 20):
        break
    time.sleep(0.02)
    canv.update()

Tkinter.mainloop()


