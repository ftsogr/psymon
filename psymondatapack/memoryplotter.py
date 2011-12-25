# -*- coding: utf-8 -*-
'''
(C) Dimitris Diamantis 2011-12

This file is part of Psymon.

Psymon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Psymon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Psymon.  If not, see <http://www.gnu.org/licenses/>.
'''

import psutil
from PyQt4 import Qt,QtCore,QtGui
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
from PyQt4.QtCore import QString


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class MemoryStat:

    Memory = 0
    Swap = 1
    counter = 0
    
    def __init__(self):
        self.procValues = self.__lookup()
   
    def statistic(self):
        values = self.__lookup()
        self.procValues = values
        return values[0], values[1]
    
    def nowTime(self):
        result = Qt.QTime(0, 0)
        return result

    def __lookup(self):
        pyhmem = psutil.phymem_usage()
        virtmem = psutil.virtmem_usage()
        return [pyhmem.percent, virtmem.percent]

class TimeScaleDraw(Qwt.QwtScaleDraw):

    def __init__(self, baseTime, *args):
        Qwt.QwtScaleDraw.__init__(self, *args)
        baseTime = baseTime.currentTime()
        self.baseTime = baseTime.addSecs(-59)
 

    def label(self, value):
        nowTime = self.baseTime.addSecs(int(value))
        return Qwt.QwtText(nowTime.toString())



class Background(Qwt.QwtPlotItem):

    def __init__(self):
        Qwt.QwtPlotItem.__init__(self)
        self.setZ(0.0)

    def rtti(self):
        return Qwt.QwtPlotItem.Rtti_PlotUserItem

    def draw(self, painter, xMap, yMap, rect):
        c = Qt.QColor(Qt.Qt.magenta)
        r = Qt.QRect(rect)

        for i in range(100, 0, -5):
            r.setBottom(yMap.transform(i - 5))
            r.setTop(yMap.transform(i))
            c.setAlpha(100)
            painter.fillRect(r, c)
            c = c.light(105)

class MemoryCurve(Qwt.QwtPlotCurve):

    def __init__(self, *args):
        Qwt.QwtPlotCurve.__init__(self, *args)
        self.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)


    def setColor(self, color):
        c = Qt.QColor(color)
        c.setAlpha(180)
        self.setPen(c)
        c.setAlpha(80)
        self.setBrush(c)


    
HISTORY = 60

class MemoryPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.curves = {}
        self.data = {}
        self.timeData = 1.0 * arange(HISTORY-1, -1, -1)
        self.memoryStat = MemoryStat()

        self.setAutoReplot(False)

        self.plotLayout().setAlignCanvasToScales(True)
        
        legend = Qwt.QwtLegend()
        legend.setItemMode(Qwt.QwtLegend.CheckableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        
        self.setAxisScaleDraw(
            Qwt.QwtPlot.xBottom, TimeScaleDraw(self.memoryStat.nowTime()))
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0, HISTORY)
        self.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -05.0)
        self.setAxisLabelAlignment(
            Qwt.QwtPlot.xBottom, Qt.Qt.AlignLeft | Qt.Qt.AlignBottom)

        self.yLeft = Qwt.QwtText(QtGui.QApplication.translate("MainWindow","Usage [%]", 
                            None, QtGui.QApplication.UnicodeUTF8))        
        self.setAxisTitle(Qwt.QwtPlot.yLeft, self.yLeft)
        self.setAxisScale(Qwt.QwtPlot.yLeft, 0, 100)
        self.setMinimumHeight(130)

        background = Background()
        background.attach(self)
     
     
        
        curve = MemoryCurve('Memory')
        curve.setColor(Qt.Qt.yellow)
        curve.attach(self)
        self.curves['Memory'] = curve
        self.data['Memory'] = zeros(HISTORY, Float)

        curve = MemoryCurve('Swap')
        curve.setColor(Qt.Qt.green)
        curve.setZ(curve.z() - 1.0)
        curve.attach(self)
        self.curves['Swap'] = curve
        self.data['Swap'] = zeros(HISTORY, Float)

        self.showCurve(self.curves['Memory'], True)
        self.showCurve(self.curves['Swap'], True)

        self.startTimer(1000)

        self.connect(self,
                     Qt.SIGNAL('legendChecked(QwtPlotItem*, bool)'),
                     self.showCurve)
        self.replot()

    
    def timerEvent(self, e):
        
        for data in self.data.values():
            data[1:] = data[0:-1]
        self.data["Memory"][0], self.data["Swap"][0] = self.memoryStat.statistic()

        self.timeData += 1.0

        self.setAxisScale(
            Qwt.QwtPlot.xBottom, self.timeData[-1], self.timeData[0])
        for key in self.curves.keys():
            self.curves[key].setData(self.timeData, self.data[key])

        self.replot()

    
    def showCurve(self, item, on):
        item.setVisible(on)
        widget = self.legend().find(item)
        if isinstance(widget, Qwt.QwtLegendItem):
            widget.setChecked(on)
        self.replot()


    def memoryPlotCurve(self, key):
        return self.curves[key]
