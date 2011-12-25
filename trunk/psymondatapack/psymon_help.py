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

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
    
class Ui_Psymon_Help(object):
    def setupUi(self, Psymon_Help):
        Psymon_Help.setObjectName(_fromUtf8("Psymon_Help"))
        Psymon_Help.resize(680, 450)
        Psymon_Help.setWindowTitle(QtGui.QApplication.translate("Psymon_Help", "Psymon Help", None, QtGui.QApplication.UnicodeUTF8))
        
        self.gridLayout_set = QtGui.QGridLayout(Psymon_Help)
        self.gridLayout_set.setObjectName(_fromUtf8("gridLayout_set"))
        
        self.label = QtGui.QTextEdit(Psymon_Help)
        self.label.setReadOnly(True)
        self.label.setAutoFillBackground(True)
        self.label.setText(QtGui.QApplication.translate("Psymon_Help","<h4>Introduction</h4>Python System Monitor (<i>Psymon</i>)<br> is a cross-platform, task and performance monitor.<br><br>Fearures:<br>*Global process monitoring<br>*System load history (cpu,memory,netwok and disks)<br>*Disks informations<br>*Network connections<br>*Detailed informations and cpu, memory percentage history per process",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_Help","<h4>Getting started</h4>The Psymon main window consists of a menu bar, the work space and a status bar.<br>The worksheets of the Psymon are: <b><i>Process Table, Cpu & Memory Info, Disks Info, Network Info</b></i> and <b><i>Detailed Process Info</b></i>. The <i>Process Table</i> lists the running processes with many informations about them. The <i>Cpu & Memory Info</i> worksheet shows graphs of system utilization: Cpu history and Memory-Swap history. The <i>Disks Info</i> worksheet shows a graph and a table of disks utilization and informations. The <i>Network Info</i> worksheet shows a graph and a table of network interfaces utilization and informations.Also shows a table with the global network connections.The <i>Detailed Process Info</i> worksheet shows a graph and three tables with informations of one selected process from the <i>Process Table</i> worksheet.",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_Help","<h4>Process Table</h4>The Process Table gives you a list of processes on your system. The list can be sorted by each column. Just press the left mouse button at the head of the column. If you have selected one process you can press the End Process button to terminate it. If this applications still have unsaved data this data will be lost. So use this button with care. The <i>Quick Search...</i> filter which processes are shown by the text given here. The text can be a partial string match of the Name, Pid or Username of the process. The compobox in the right of the <i>Quick Search...</i> can used to change the process table in <i>Table View</i> or <i>Tree View</i>. Also if you perform a double left click on a process you moved to the <i>Detailed Process Info</i> worksheet where you can see detailed informations about this process.",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_Help","<h4>Graphs</h4>The graphs of the Psymon on the axis Y shows percentage or KiloBytes (KB) and on the axis X the time. On the right side of every graph-box there are buttons that can be used to show or hide graphs.",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_Help","<br><i>Note:</i> The multiples of a byte in Psymon are decimals and not binaries. For example, a KiloByte is 1000 bytes and not 1024 bytes, which is a KibiByte.",None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_set.addWidget(self.label, 0, 0, 0, 0)