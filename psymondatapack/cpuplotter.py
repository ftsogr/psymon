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
import os
from PyQt4 import Qt,QtCore,QtGui
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
from PyQt4.QtCore import QString


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class CpuStat:

    User = 0
    Nice = 1
    System = 2
    Idle = 3
    counter = 0
    
    def __init__(self):
        self.procValues = self.__lookup()
  
    def statistic(self):
        values = self.__lookup()
        userDelta = 0.0
        for i in [CpuStat.User, CpuStat.Nice]:
            userDelta += (values[i] - self.procValues[i])
        systemDelta = values[CpuStat.System] - self.procValues[CpuStat.System]
        totalDelta = 0.0
        for i in range(len(self.procValues)):
            totalDelta += (values[i] - self.procValues[i])
        self.procValues = values
        return 100.0*userDelta/totalDelta, 100.0*systemDelta/totalDelta
    
    
    def nowTime(self):
        result = Qt.QTime(0, 0)
        return result

    def __lookup(self):
        mycputimes=psutil.cpu_times(percpu=False)
        if os.name == "nt":
            tmp = [mycputimes.user,0.0,mycputimes.system,mycputimes.idle,0.0,0.0,0.0]
        else:
            tmp = [mycputimes.user,mycputimes.nice,mycputimes.system,mycputimes.idle,mycputimes.iowait,mycputimes.irq,mycputimes.softirq]
        return tmp

class CpuPieMarker(Qwt.QwtPlotMarker):
    
    def __init__(self, *args):
        Qwt.QwtPlotMarker.__init__(self, *args)
        self.setZ(1000.0)
        self.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, True)
        
    def rtti(self):
        return Qwt.QwtPlotItem.Rtti_PlotUserItem

    def draw(self, painter, xMap, yMap, rect):
        margin = 5
        pieRect = Qt.QRect()
        pieRect.setX(rect.x() + margin)
        pieRect.setY(rect.y() + margin)
        pieRect.setHeight(yMap.transform(80.0))
        pieRect.setWidth(pieRect.height())

        angle = 3*5760/4
        for key in ["User", "System", "Idle"]:
            curve = self.plot().cpuPlotCurve(key)
            if curve.dataSize():
                value = int(5760*curve.y(0)/100.0)
                painter.save()
                painter.setBrush(Qt.QBrush(curve.pen().color(),
                                              Qt.Qt.SolidPattern))
                painter.drawPie(pieRect, -angle, -value)
                painter.restore()
                angle += value


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
        c = Qt.QColor(Qt.Qt.red)
        r = Qt.QRect(rect)

        for i in range(100, 0, -5):
            r.setBottom(yMap.transform(i - 5))
            r.setTop(yMap.transform(i))
            c.setAlpha(100)
            painter.fillRect(r, c)
            c = c.light(105)

class CpuCurve(Qwt.QwtPlotCurve):

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

class CpuPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.curves = {}
        self.data = {}
        self.timeData = 1.0 * arange(HISTORY-1, -1, -1)
        self.cpuStat = CpuStat()

        self.setAutoReplot(False)

        self.plotLayout().setAlignCanvasToScales(True)
        
        legend = Qwt.QwtLegend()
        legend.setItemMode(Qwt.QwtLegend.CheckableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        
        self.setAxisScaleDraw(
            Qwt.QwtPlot.xBottom, TimeScaleDraw(self.cpuStat.nowTime()))
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

        pie = CpuPieMarker()
        pie.attach(self)
        
        curve = CpuCurve('System')
        curve.setColor(Qt.Qt.green)
        curve.attach(self)
        self.curves['System'] = curve
        self.data['System'] = zeros(HISTORY, Float)

        curve = CpuCurve('User')
        curve.setColor(Qt.Qt.blue)
        curve.setZ(curve.z() - 1.0)
        curve.attach(self)
        self.curves['User'] = curve
        self.data['User'] = zeros(HISTORY, Float)

        curve = CpuCurve('Total')
        curve.setColor(Qt.Qt.black)
        curve.setZ(curve.z() - 2.0)
        curve.attach(self)
        self.curves['Total'] = curve
        self.data['Total'] = zeros(HISTORY, Float)

        curve = CpuCurve('Idle')
        curve.setColor(Qt.Qt.darkCyan)
        curve.setZ(curve.z() - 3.0)
        curve.attach(self)
        self.curves['Idle'] = curve
        self.data['Idle'] = zeros(HISTORY, Float)

        self.showCurve(self.curves['System'], True)
        self.showCurve(self.curves['User'], True)
        self.showCurve(self.curves['Total'], False)
        self.showCurve(self.curves['Idle'], False)

        self.startTimer(1000)

        self.connect(self,
                     Qt.SIGNAL('legendChecked(QwtPlotItem*, bool)'),
                     self.showCurve)
        self.replot()

    
    def timerEvent(self, e):
        for data in self.data.values():
            data[1:] = data[0:-1]
        self.data["User"][0], self.data["System"][0] = self.cpuStat.statistic()
        self.data["Total"][0] = self.data["User"][0] + self.data["System"][0]
        self.data["Idle"][0] = 100.0 - self.data["Total"][0]

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


    def cpuPlotCurve(self, key):
        return self.curves[key]
