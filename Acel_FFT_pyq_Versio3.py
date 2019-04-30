# -*- coding: utf-8 -*-
import sys
import glob
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from collections import deque  # import a "circular" list
from threading import Thread, Lock

#Reads the available serial ports
if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')

result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
        pass
print(result)

usb = input('Entre com a porta desejada: ')

arduinoData = serial.Serial(usb, 115200)  # 115200


freq = 2000              # 1/T
guarda = 500             # 500

frequencia = np.linspace(0.0, 1.0/(2.0*(1/freq)), int(guarda/2))

acelx = deque([], maxlen=guarda)

win = pg.GraphicsWindow()
win.setWindowTitle('Espectro')
pg.setConfigOption('foreground', 'w')

p1 = win.addPlot(
    title="<span style='color: #ffffff; font-weight: bold; font-size:20px'>Accelerometer</span>")
linha1 = pg.mkPen((0, 255, 0), width=2)  # style=QtCore.Qt.DashLine)
p1.addLegend(offset=(10, 5))

curve1 = p1.plot(acelx,
                 pen=linha1,
                 name="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>X</span>")

p1.setRange(yRange=[-5, 5])
p1.setLabel('bottom',
            text="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Time</span>")
p1.showGrid(x=True, y=False)

win.nextRow()
p2 = win.addPlot()
linha4 = pg.mkPen((255, 0, 0), width=2)
p2.addLegend(offset=(10, 5))

curve2 = p2.plot(acelx,
                 pen=linha4,
                 name="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Amplitude</span>")

p2.setRange(xRange=[0, int(freq/2)])
p2.setLabel('bottom',
            text="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Frequency (Hz)</span>")
p2.showGrid(x=False, y=True)
ax = p2.getAxis('bottom')
ax.setTicks([[(v, str(v)) for v in np.arange(0, int(freq/2)+1, 100)]])

i = 0
data = []
lock = Lock()
def data_input():
    global i, data
    for line in arduinoData:
        try:
            i+=1
            acelx.append(float(line))
            with lock:
                if i > len(acelx):
                    data = np.fft.fft(acelx)
        except ValueError:
            pass

# start the data input thread. This will run in the background unaffected by the GUI.
t = Thread(target=data_input)
t.daemon = True
t.start()

def update():
    curve1.setData(acelx)
    if i > len(acelx):
        curve2.setData(frequencia, (2/guarda * np.abs(data[0:np.int(guarda/2)])))

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
