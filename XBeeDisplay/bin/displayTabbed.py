from math import floor
import csv
from datetime import datetime, timezone, timedelta
import sys

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets


"""
    This program, designed to be run in conjunction with xbee.py, displays data in "real-time" coming directly from the
    the .csv file outputted by xbee.py through pyqtgraph.
"""

data = [[], [], [], [], [], [], []]
offset = 0

## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# initialize the window
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.setWindowTitle("Data")
mw.resize(1500, 1000)

# initialize tabs and tab container
ccw = QtGui.QTabWidget()
cw = QtGui.QWidget()
cwHist = QtGui.QWidget()
ccw.addTab(cw, "Live")
ccw.addTab(cwHist, "Historical")
mw.setCentralWidget(ccw)

# initialize tab layouts
l = QtGui.QGridLayout()
cw.setLayout(l)
lHist = QtGui.QGridLayout()
cwHist.setLayout(lHist)

# TODO Dynamic number of channels
# initializes the plots one plot at a time
pAD0 = pg.PlotWidget(title="ADO (Last 20 packets)", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve0 = pAD0.plot(pen=pg.mkPen('b', width=2))
l.addWidget(pAD0, 0, 0)

pAD1 = pg.PlotWidget(title="AD1 (Last 20 packets)", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve1 = pAD1.plot(pen=pg.mkPen('b', width=2))
l.addWidget(pAD1, 0, 1)

pAD2 = pg.PlotWidget(title="AD2 (Last 20 packets)", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve2 = pAD2.plot(pen=pg.mkPen('b', width=2))
l.addWidget(pAD2, 0, 2)

pAD3 = pg.PlotWidget(title="AD3 (Last 20 packets)", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve3 = pAD3.plot(pen=pg.mkPen('b', width=2))
l.addWidget(pAD3, 1, 0)

pAD4 = pg.PlotWidget(title="AD4 (Last 20 packets)", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve4 = pAD4.plot(pen=pg.mkPen('b', width=2))
l.addWidget(pAD4, 1, 1)

pSigStrength = pg.PlotWidget(title="Signal Strength (Last 20 packets)", labels={'left': "Signal Strength (dBm)",
                                                                       'bottom': "Time (s)"})
curveSig = pSigStrength.plot(pen=pg.mkPen('b', width=2))
pSigStrength.setYRange(0, -100, padding=0.02)
l.addWidget(pSigStrength, 1, 2)

# intialize historical plots
pAD0Hist = pg.PlotWidget(title="ADO", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve0Hist = pAD0Hist.plot(pen=pg.mkPen('b', width=2))
pAD0Hist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pAD0Hist, 0, 0)

pAD1Hist = pg.PlotWidget(title="AD1", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve1Hist = pAD1Hist.plot(pen=pg.mkPen('b', width=2))
pAD1Hist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pAD1Hist, 0, 1)

pAD2Hist = pg.PlotWidget(title="AD2", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve2Hist = pAD2Hist.plot(pen=pg.mkPen('b', width=2))
pAD2Hist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pAD2Hist, 0, 2)

pAD3Hist = pg.PlotWidget(title="AD3", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve3Hist = pAD3Hist.plot(pen=pg.mkPen('b', width=2))
pAD3Hist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pAD3Hist, 1, 0)

pAD4Hist = pg.PlotWidget(title="AD4", labels={'left': "Resistance (kiloohms)", 'bottom': "Time (s)"})
curve4Hist = pAD4Hist.plot(pen=pg.mkPen('b', width=2))
pAD4Hist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pAD4Hist, 1, 1)

pSigHist = pg.PlotWidget(title="Signal Strength", labels={'left': "Signal Strength (dBm)",
                                                            'bottom': "Time (s)"})
curveSigHist = pSigHist.plot(pen=pg.mkPen('b', width=2))
pSigHist.setYRange(0, -100, padding=0.02)
pSigHist.setXRange(0, 20, padding = 0.02)
lHist.addWidget(pSigHist, 1, 2)

# creates the date entry widget for input in the historical database
dateEdit = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
dateEdit.setDisplayFormat("yyyy.MM.dd HH:mm:ss")

# updates plot xrange to the time specified by the date widget
@QtCore.pyqtSlot()
def on_click():
    # gets date and time from dateEdit
    y = int(dateEdit.sectionText(dateEdit.sectionAt(0)))
    m = int(dateEdit.sectionText(dateEdit.sectionAt(1)))
    d = int(dateEdit.sectionText(dateEdit.sectionAt(2)))
    h = int(dateEdit.sectionText(dateEdit.sectionAt(3)))
    mi = int(dateEdit.sectionText(dateEdit.sectionAt(4)))
    s = int(dateEdit.sectionText(dateEdit.sectionAt(5)))
    goto = (datetime(y, m, d, h, mi, s, 0, timezone(timedelta(hours=offset))).timestamp())

    # if it is later than the end of the dataHist, just go to the end
    if goto * 1000 > data[6][len(data[6])-1]:
        pAD0Hist.setXRange(len(data[6])-20, len(data[6]))
        pAD1Hist.setXRange(len(data[6])-20, len(data[6]))
        pAD2Hist.setXRange(len(data[6])-20, len(data[6]))
        pAD3Hist.setXRange(len(data[6])-20, len(data[6]))
        pAD4Hist.setXRange(len(data[6])-20, len(data[6]))
        pSigHist.setXRange(len(data[6])-20, len(data[6]))

    # or if it is earlier, just go to the start
    elif goto*1000 < data[6][0]:
        pAD0Hist.setXRange(0, 20)
        pAD1Hist.setXRange(0, 20)
        pAD2Hist.setXRange(0, 20)
        pAD3Hist.setXRange(0, 20)
        pAD4Hist.setXRange(0, 20)
        pSigHist.setXRange(0, 20)

    # go to the packet that is the closest to the time given and center on it
    else:
        index = data[6].index(min(data[6], key=lambda x: abs(x-goto*1000)))
        pAD0Hist.setXRange(index-10, index+10)
        pAD1Hist.setXRange(index-10, index+10)
        pAD2Hist.setXRange(index-10, index+10)
        pAD3Hist.setXRange(index-10, index+10)
        pAD4Hist.setXRange(index-10, index+10)
        pSigHist.setXRange(index-10, index+10)

# initialize button that actually goes to the point requested and adds the widgets
button = QtWidgets.QPushButton("GO TO")
button.clicked.connect(on_click)
lHist.addWidget(dateEdit, 2, 0, 1, 2)
lHist.addWidget(button, 2, 2, 1, 1)

# creates entry for UTC offset for dataHist
offsetEdit = QtGui.QSpinBox()
offsetEdit.setMinimum(-14)
offsetEdit.setMaximum(14)

# updates plot offset to the offset specified by the user
@QtCore.pyqtSlot()
def on_click2():
    global offset
    offset = offsetEdit.value()
    updateHist()

# initializes button that actually changes the UTC offset and adds the widgets
button2 = QtWidgets.QPushButton("UPDATE UTC OFFSET")
button2.clicked.connect(on_click2)
lHist.addWidget(offsetEdit, 3, 0, 1, 2)
lHist.addWidget(button2, 3, 2, 1, 1)

# now - display!
mw.show()

def adValtoR(val):
    """
        Converts the value received from the XBee to an actual resistance value.

        Return resistance in kiloohms, or -1 if there is no connection/if the
        resistance is too high to measure.
    """
    if val == 0:
        return 0
    elif val == 1023:
        return -1
    else:
        return 1/(float(1023)/(val)-1)*5.2

def update():
    """
        Updates the graphs from the .csv file.

        Assumes that the .csv file is generated in a very specific manner, possibly specific to this installation of
        Python.
        Averages the samples in each packet to receive a value, this situation might need to be changed if packet rates
        decrease but sample numbers remain the same.
    """

    # TODO ensure that this works on all systems
    global curve0, curve1, curve2, curve3, curve4, pAD0, data
    data = [[], [], [], [], [], [], []]

    # opens the csv to read, so it doesn't lock the file
    with open('origData.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        current_packet_data = [[], [], [], [], []]
        n = 0
        packetN = 0

        # reads each row in the .csv to create an array
        # TODO skip earlier rows in the .csv
        # TODO perhaps actually detect if the rows are empty
        for row in reader:
            # if the rows are empty, don't bother
            if n % 2 == 1:
                n += 1
                continue
            if n == 0:
                packet = row[0]
            n += 1

            # if the row is in the packet we are currently processing, add it to the current packet
            if row[0] == str(packet):
                current_packet_data[0].append(adValtoR(int(row[3])))
                current_packet_data[1].append(adValtoR(int(row[4])))
                current_packet_data[2].append(adValtoR(int(row[5])))
                current_packet_data[3].append(adValtoR(int(row[6])))
                current_packet_data[4].append(adValtoR(int(row[7])))
            # otherwise we're done with this packet, and we average its dataHist and add it to the array
            # TODO also this signal strength might be from this next packet (might not be that important)
            else:
                data[0].append(sum(current_packet_data[0]) / float(len(current_packet_data[0])))
                data[1].append(sum(current_packet_data[1]) / float(len(current_packet_data[1])))
                data[2].append(sum(current_packet_data[2]) / float(len(current_packet_data[2])))
                data[3].append(sum(current_packet_data[3]) / float(len(current_packet_data[3])))
                data[4].append(sum(current_packet_data[4]) / float(len(current_packet_data[4])))
                data[5].append(int(row[2][0:3]))
                data[6].append(float(row[0]))

                # if there has been a discontinuity in the dataHist, we mark it with a significant deviation.
                if(float(packet) - float(row[0]) < -5000):
                    data[0].append(-5)
                    data[1].append(-5)
                    data[2].append(-5)
                    data[3].append(-5)
                    data[4].append(-5)
                    data[5].append(5)
                    data[6].append((float(packet)+float(row[0]))/2)

                # then we clear the current dataHist out, add this packet's dataHist to the new array,
                # and increment the packet number
                current_packet_data = [[], [], [], [], []]
                current_packet_data[0].append(adValtoR(int(row[3])))
                current_packet_data[1].append(adValtoR(int(row[4])))
                current_packet_data[2].append(adValtoR(int(row[5])))
                current_packet_data[3].append(adValtoR(int(row[6])))
                current_packet_data[4].append(adValtoR(int(row[7])))
                packet = row[0]
                packetN += 1
    curve0.setData(data[0][max(packetN - 20, 0):packetN])
    curve1.setData(data[1][max(packetN - 20, 0):packetN])
    curve2.setData(data[2][max(packetN - 20, 0):packetN])
    curve3.setData(data[3][max(packetN - 20, 0):packetN])
    curve4.setData(data[4][max(packetN - 20, 0):packetN])
    curveSig.setData(data[5][max(packetN - 20, 0):packetN])


# update the graph every 1000ms (one second) - this could be configurable
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)

def ticks(dataHist):
    """
        Creates an array representing the ticks at the bottom of the screen for every twenty packets,
        to be used by pyqtgraph.
    """
    first = [(dataHist[6].index(v), str(datetime.fromtimestamp(v/1000.0, timezone.utc).astimezone(timezone(timedelta(hours=offset))))) for v in dataHist[6]]
    second = [first[v*20] for v in range(0, int(floor(len(dataHist[6])/20)))]
    return [second, []]

def updateHist():
    """
        Updates the graphs from the .csv file.

        Assumes that the .csv file is generated in a very specific manner, possibly specific to this installation of
        Python.
        Averages the samples in each packet to receive a value, this situation might need to be changed if packet rates
        decrease but sample numbers remain the same.
    """

    # TODO ensure that this works on all systems
    global curve0Hist, curve1Hist, curve2Hist, curve3Hist, curve4Hist, pAD0Hist, data

    # graph!
    curve0Hist.setData(data[0])
    pAD0Hist.getAxis("bottom").setTicks(ticks(data))
    pAD0Hist.setYRange(-5, 10, padding=0.02)
    curve1Hist.setData(data[1])
    pAD1Hist.getAxis("bottom").setTicks(ticks(data))
    pAD1Hist.setYRange(-5, 10, padding=0.02)
    curve2Hist.setData(data[2])
    pAD2Hist.getAxis("bottom").setTicks(ticks(data))
    pAD2Hist.setYRange(-5, 10, padding=0.02)
    curve3Hist.setData(data[3])
    pAD3Hist.getAxis("bottom").setTicks(ticks(data))
    pAD3Hist.setYRange(-5, 10, padding=0.02)
    curve4Hist.setData(data[4])
    pAD4Hist.getAxis("bottom").setTicks(ticks(data))
    pAD4Hist.setYRange(-5, 10, padding=0.02)
    curveSigHist.setData(data[5])
    pSigHist.getAxis("bottom").setTicks(ticks(data))

# updates the graph for the first time
updateHist()

# updateHist the graph every 30000ms (thirty seconds) - this could be configurable
timerHist = QtCore.QTimer()
timerHist.timeout.connect(updateHist)
timerHist.start(1000*30)

if __name__ == '__main__':
    # now we actually display it
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
