# -*- coding: utf-8 -*-
import sys
import glob
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

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

usb = input('Select the serial port: ')

arduinoData = serial.Serial(usb, 115200)  # 115200

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

acelz = []

freq = 2000              # 1/T   -> T is the arduino delay in seconds
guarda = 500             # Buffer for the FFT, higher value equals better resolution
r = range(0, int(freq/2+1), int(freq/guarda))

win = pg.GraphicsWindow()
win.setWindowTitle('Spectrum')
pg.setConfigOption('foreground', 'w')

p1 = win.addPlot(
    title="<span style='color: #ffffff; font-weight: bold; font-size:20px'>Spectrum</span>")
linha1 = pg.mkPen((0, 255, 0), width=2)  # style=QtCore.Qt.DashLine)
linha2 = pg.mkPen((0, 0, 255), width=2)  # style=QtCore.Qt.DashLine)
linha3 = pg.mkPen((255, 0, 0), width=2)  # style=QtCore.Qt.DashLine)
p1.addLegend(offset=(10, 5))

curve1 = p1.plot(acelz,
                 pen=linha1,
                 name="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Z axis</span>")

p1.setRange(yRange=[-3, 3])
p1.setLabel('bottom',
            text="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Time</span>")
p1.showGrid(x=True, y=False)

win.nextRow()
p2 = win.addPlot()
linha4 = pg.mkPen((255, 0, 0), width=2)
p2.addLegend(offset=(10, 5))

curve2 = p2.plot(acelz,
                 pen=linha4,
                 name="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Amplitude</span>")

p2.setRange(yRange=[0, 1000], xRange=[0, 500])
p2.setLabel('bottom',
            text="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Frequency (Hz)</span>")
p2.showGrid(x=False, y=True)

i = 0

def update():
    global i
    try:
        arduinoString = ReadLine(arduinoData)
        dataArray = arduinoString.readline().decode("utf-8").split(',')

        acelerometroz = int(dataArray[0])/4096.0   # 16384, 8192, 4096, 2048 for accelerometer set 2, 4, 8, 16g

        acelz.append(acelerometroz)
        
        #np.savetxt("Accelerometer-FFT---Real-time\Data\Data.csv", acelz, delimiter=",")

        if i > guarda:
            try:
                data = np.fft.fft(acelz[-guarda:])
                frequencia = np.fft.fftfreq(len(data), d=1/freq)
            except IOError:
                pass
            curve2.setData(frequencia[:int(guarda/2)], abs(np.real(data[:int(guarda/2)]))**2)

        curve1.setData(acelz)
        i += 1
        curve1.setPos(i, 0)
        if i > guarda:
            del acelz[0:1]

    except ValueError:
        pass

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)  

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
