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
    
    
class Ui_Psymon_About(object):
    def setupUi(self, Psymon_About):
        Psymon_About.setObjectName(_fromUtf8("Psymon_About"))
        Psymon_About.resize(450, 350)
        
        Psymon_About.setMaximumSize(450, 350)
        Psymon_About.setMinimumSize(450, 350)

        Psymon_About.setWindowTitle(QtGui.QApplication.translate("Psymon_About", "About Psymon", None, QtGui.QApplication.UnicodeUTF8))
        
        self.gridLayout_set = QtGui.QGridLayout(Psymon_About)
        self.gridLayout_set.setObjectName(_fromUtf8("gridLayout_set"))
        

        
        self.label = QtGui.QTextEdit(Psymon_About)
        self.label.setReadOnly(True)
        self.label.setAutoFillBackground(True)
        self.label.setHtml("<img src="+iconspath+"psymon.png heght=80 width=80 align=right>")
        self.label.append(QtGui.QApplication.translate("Psymon_About","<h4>About</h4>Python System Monitor (<i>Psymon</i>)<br>Cross-platform, task and performance monitor.<br>Version: ",None, QtGui.QApplication.UnicodeUTF8)+version)
        self.label.append(QtGui.QApplication.translate("Psymon_About","(<b>C</b>) 2011-2012 Dimitris Diamantis<br><br><h4>License</h4>Psymon is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 3 as published by the Free Software Foundation.<br>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/].",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_About","<br><h4>Contact</h4>Dimitris Diamantis <i>aka</i> ftso<br>email: kotsifi@gmail.com<br>website: www.ftso.gr",None, QtGui.QApplication.UnicodeUTF8))
        self.label.append(QtGui.QApplication.translate("Psymon_About","<br><h4>Credits</h4>Thanks for their support or work:<br>-The development teams of the projects:<br>PyQt4, Python, Psutil, Python(x,y), Oxygen-icons<br>-The IT professors:<br>A.Sidiropoulos and S.Harhalakis",None, QtGui.QApplication.UnicodeUTF8))

        self.gridLayout_set.addWidget(self.label, 0, 0, 0, 0)