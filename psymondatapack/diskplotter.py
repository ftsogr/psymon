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


class DiskStat:
    In = 0
    Out = 1
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

    def mbscale(self):
        result=""
        return result
        
    def __lookup(self):
        global diskdata
        try:
            disk_in=diskdata[0]
            disk_out=diskdata[1]
        except(NameError):
            disk_in=0.0
            disk_out=0.0
                
        return [disk_in,disk_out]

class TimeScaleDraw(Qwt.QwtScaleDraw):

    def __init__(self, baseTime, *args):
        Qwt.QwtScaleDraw.__init__(self, *args)
        baseTime = baseTime.currentTime()
        self.baseTime = baseTime.addSecs(-59)
 

    def label(self, value):
        nowTime = self.baseTime.addSecs(int(value))
        return Qwt.QwtText(nowTime.toString())



class NetScaleDraw(Qwt.QwtScaleDraw):
    
    def __init__(self,Qstring, *args):
        Qwt.QwtScaleDraw.__init__(self, *args)

    def label(self, value):
        mbscale = str(value)
        return Qwt.QwtText(mbscale)


class Background(Qwt.QwtPlotItem):

    def __init__(self):
        Qwt.QwtPlotItem.__init__(self)
        self.setZ(0.0)

    def rtti(self):
        return Qwt.QwtPlotItem.Rtti_PlotUserItem

    def draw(self, painter, xMap, yMap, rect):
        c = Qt.QColor(Qt.Qt.yellow)
        r = Qt.QRect(rect) 
        c.setAlpha(100)
        painter.fillRect(r, c)

class DiskCurve(Qwt.QwtPlotCurve):

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

class DiskPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.curves = {}
        self.data = {}
        self.timeData = 1.0 * arange(HISTORY-1, -1, -1)
        self.diskStat = DiskStat()

        self.setAutoReplot(False)

        self.plotLayout().setAlignCanvasToScales(True)
        
        legend = Qwt.QwtLegend()
        legend.setItemMode(Qwt.QwtLegend.CheckableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        
        self.xBottom_title = Qwt.QwtText(QtGui.QApplication.translate("MainWindow","Timeline 60sec [h:m:s]", 
                            None, QtGui.QApplication.UnicodeUTF8))
        self.setAxisTitle(Qwt.QwtPlot.xBottom, self.xBottom_title)
        self.setAxisScaleDraw(
            Qwt.QwtPlot.xBottom, TimeScaleDraw(self.diskStat.nowTime()))
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0, HISTORY)
        self.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -05.0)
        self.setAxisLabelAlignment(
            Qwt.QwtPlot.xBottom, Qt.Qt.AlignLeft | Qt.Qt.AlignBottom)

        self.yLeft = Qwt.QwtText(QtGui.QApplication.translate("MainWindow","Usage [KB]", 
                            None, QtGui.QApplication.UnicodeUTF8))        
        self.setAxisTitle(Qwt.QwtPlot.yLeft, self.yLeft)
        
        self.setAxisScaleDraw(
            Qwt.QwtPlot.yLeft, NetScaleDraw(self.diskStat.mbscale()))
        
        self.setMinimumHeight(140)
        
        Qwt.QwtPlot.setAxisAutoScale(self,Qwt.QwtPlot.yLeft)

        background = Background()
        background.attach(self)
             
        curve = DiskCurve('Write')
        curve.setColor(Qt.Qt.magenta)
        curve.attach(self)
        self.curves['Write'] = curve
        self.data['Write'] = zeros(HISTORY, Float)

        curve = DiskCurve('Read')
        curve.setColor(Qt.Qt.green)
        curve.setZ(curve.z() - 1.0)
        curve.attach(self)
        self.curves['Read'] = curve
        self.data['Read'] = zeros(HISTORY, Float)

        self.showCurve(self.curves['Write'], True)
        self.showCurve(self.curves['Read'], True)

        self.startTimer(1000)

        self.connect(self,
                     Qt.SIGNAL('legendChecked(QwtPlotItem*, bool)'),
                     self.showCurve)
        
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableX(False)
        self.grid.attach(self)

        global diskdata,new_paint
        diskdata = [0,0]
        new_paint = True

    def disk_data(self):
        if _disk == "None":
            return psutil.disk_io_counters(perdisk=False)        
        else:
            return psutil.disk_io_counters(perdisk=True)[_disk]
                
    
    def timerEvent(self, e):
        
        for data in self.data.values():
            data[1:] = data[0:-1]
        self.data["Write"][0], self.data["Read"][0] = self.diskStat.statistic()

        self.timeData += 1.0

        self.setAxisScale(
            Qwt.QwtPlot.xBottom, self.timeData[-1], self.timeData[0])

        self.setAxisScaleDraw(
            Qwt.QwtPlot.yLeft, NetScaleDraw(self))  
        
        for key in self.curves.keys():
            self.curves[key].setData(self.timeData, self.data[key])
               
        
        global write_a,read_a,diskdata,new_paint
        
        if new_paint == True:
            diskdata = [0.0,0.0]
            write_a = ""
            read_a = ""
            new_paint = False
        else:
            write_b = self.disk_data().write_bytes
            read_b = self.disk_data().read_bytes
        
            try:
                diskdata = [(write_b-write_a)/1000.0,(read_b-read_a)/1000.0]
            except(NameError,TypeError):
                diskdata = [0.0,0.0]
            
            write_a = self.disk_data().write_bytes
            read_a = self.disk_data().read_bytes
        
        self.replot()

    
    def showCurve(self, item, on):
        item.setVisible(on)
        widget = self.legend().find(item)
        if isinstance(widget, Qwt.QwtLegendItem):
            widget.setChecked(on)
        self.replot()


    def diskPlotCurve(self, key):
        return self.curves[key]
