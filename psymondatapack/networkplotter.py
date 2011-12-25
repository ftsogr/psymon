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


class NetworkStat:
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
        result=0.0
        return result
        
    def __lookup(self):
        global netdata
        try:
            net_in=netdata[0]
            net_out=netdata[1]
        except(NameError):
            net_in=0.0
            net_out=0.0
                
        return [net_in,net_out]

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
        c = Qt.QColor(Qt.Qt.cyan)
        r = Qt.QRect(rect)
        c.setAlpha(100)
        painter.fillRect(r, c)



class NetworkCurve(Qwt.QwtPlotCurve):

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

class NetworkPlot(Qwt.QwtPlot):

    def __init__(self, *args):

        Qwt.QwtPlot.__init__(self, *args)

        self.curves = {}
        self.data = {}
        self.timeData = 1.0 * arange(HISTORY-1, -1, -1)
        self.networkStat = NetworkStat()

        self.setAutoReplot(False)

        self.plotLayout().setAlignCanvasToScales(True)
        
        legend = Qwt.QwtLegend()
        legend.setItemMode(Qwt.QwtLegend.CheckableItem)
        self.insertLegend(legend, Qwt.QwtPlot.RightLegend)
        
        self.xBottom_title = Qwt.QwtText(QtGui.QApplication.translate("MainWindow","Timeline 60sec [h:m:s]", 
                            None, QtGui.QApplication.UnicodeUTF8))
        self.setAxisTitle(Qwt.QwtPlot.xBottom, self.xBottom_title)
        self.setAxisScaleDraw(
            Qwt.QwtPlot.xBottom, TimeScaleDraw(self.networkStat.nowTime()))
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0, HISTORY)
        self.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -05.0)
        self.setAxisLabelAlignment(
            Qwt.QwtPlot.xBottom, Qt.Qt.AlignLeft | Qt.Qt.AlignBottom)

        self.yLeft = Qwt.QwtText(QtGui.QApplication.translate("MainWindow","Usage [KB]", 
                            None, QtGui.QApplication.UnicodeUTF8))        
        self.setAxisTitle(Qwt.QwtPlot.yLeft, self.yLeft)
        
        self.setAxisScaleDraw(
            Qwt.QwtPlot.yLeft, NetScaleDraw(self.networkStat.mbscale()))
        
        self.setMinimumHeight(140)
        
        Qwt.QwtPlot.setAxisAutoScale(self,Qwt.QwtPlot.yLeft)

        background = Background()
        background.attach(self)
     
        curve = NetworkCurve('Net In')
        curve.setColor(Qt.Qt.green)
        curve.attach(self)
        self.curves['Net In'] = curve
        self.data['Net In'] = zeros(HISTORY, Float)

        curve = NetworkCurve('Net Out')
        curve.setColor(Qt.Qt.blue)
        curve.setZ(curve.z() - 1.0)
        curve.attach(self)
        self.curves['Net Out'] = curve
        self.data['Net Out'] = zeros(HISTORY, Float)

        self.showCurve(self.curves['Net In'], True)
        self.showCurve(self.curves['Net Out'], True)

        self.startTimer(1000)

        self.connect(self,
                     Qt.SIGNAL('legendChecked(QwtPlotItem*, bool)'),
                     self.showCurve)
        
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableX(False)
        self.grid.attach(self)
        
        
        global netdata,new_paint
        netdata = [0.0,0.0]
        new_paint = True
        

    def net_data(self):
        if _netif == "None":
            return psutil.network_io_counters(pernic=False)
        else: 
            return psutil.network_io_counters(pernic=True)[_netif]

    
    def timerEvent(self, e):
        
        for data in self.data.values():
            data[1:] = data[0:-1]
        self.data["Net In"][0], self.data["Net Out"][0] = self.networkStat.statistic()

        self.timeData += 1.0

        self.setAxisScale(
            Qwt.QwtPlot.xBottom, self.timeData[-1], self.timeData[0])

        self.setAxisScaleDraw(
            Qwt.QwtPlot.yLeft, NetScaleDraw(self))  
        
        for key in self.curves.keys():
            self.curves[key].setData(self.timeData, self.data[key])
         
         
         
        global in_a,out_a,netdata,new_paint
        
        if new_paint == True:
            netdata = [0.0,0.0]
            in_a = ""
            out_a = ""
            new_paint = False
        else:
            in_b = self.net_data().bytes_recv
            out_b = self.net_data().bytes_sent        
            try:
                netdata = [(in_b-in_a)/1000.0,(out_b-out_a)/1000.0]
            except(NameError,TypeError):
                netdata = [0.0,0.0]
            
            in_a = self.net_data().bytes_recv
            out_a = self.net_data().bytes_sent

        
        self.replot()
    
    def showCurve(self, item, on):
        item.setVisible(on)
        widget = self.legend().find(item)
        if isinstance(widget, Qwt.QwtLegendItem):
            widget.setChecked(on)
        self.replot()
        


    def networkPlotCurve(self, key):
        return self.curves[key]
