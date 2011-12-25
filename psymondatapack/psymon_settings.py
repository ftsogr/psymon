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

class Ui_Psymon_Settings(object):
    def setupUi(self, Psymon_Settings):
        Psymon_Settings.setObjectName(_fromUtf8("Psymon_Settings"))
        Psymon_Settings.resize(100, 100)
        Psymon_Settings.setWindowTitle(QtGui.QApplication.translate("Psymon_Settings", "Psymon Settings", None, QtGui.QApplication.UnicodeUTF8))
        
        self.gridLayout_set = QtGui.QGridLayout(Psymon_Settings)
        self.gridLayout_set.setObjectName(_fromUtf8("gridLayout_set"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.label = QtGui.QLabel(Psymon_Settings)
        self.label.setText(QtGui.QApplication.translate("Psymon_Settings", "Gui Style: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        
        self.comboBox = QtGui.QComboBox(Psymon_Settings)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 4)
        
        self.label_1 = QtGui.QLabel(Psymon_Settings)
        self.label_1.setText(QtGui.QApplication.translate("Psymon_Settings", "Application Language: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout.addWidget(self.label_1, 1, 0, 1, 1)
        
        self.comboBox_1 = QtGui.QComboBox(Psymon_Settings)
        self.comboBox_1.setObjectName(_fromUtf8("comboBox_1"))
        self.gridLayout.addWidget(self.comboBox_1, 1, 1, 1, 4)
        
        
        self.label_2 = QtGui.QLabel(Psymon_Settings)
        self.label_2.setText(QtGui.QApplication.translate("Psymon_Settings", "Tabs Orientation: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        
        self.comboBox_2 = QtGui.QComboBox(Psymon_Settings)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(0,"Left")
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(1,"Center")
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(2,"Right")
        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 4)
        
        self.label_3 = QtGui.QLabel(Psymon_Settings)
        self.label_3.setText(QtGui.QApplication.translate("Psymon_Settings", "Worksheet 5 Graph Timeline: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        
        self.label_5 = QtGui.QLabel(Psymon_Settings)
        self.label_5.setText(QtGui.QApplication.translate("Psymon_Settings", "minutes ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 4, 1, 1)
        
        self.comboBox_3 = QtGui.QComboBox(Psymon_Settings)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(0,"Fast")
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(1,"Medium")
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(2,"Slow")
        self.gridLayout.addWidget(self.comboBox_3, 4, 1, 1, 4)
        
        self.label_4 = QtGui.QLabel(Psymon_Settings)
        self.label_4.setText(QtGui.QApplication.translate("Psymon_Settings", "Process Table Refresh: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        
        self.spinBox_set = QtGui.QSpinBox(Psymon_Settings)
        self.spinBox_set.setObjectName(_fromUtf8("spinBox_set"))
        self.gridLayout.addWidget(self.spinBox_set, 3, 1, 1, 3)
        self.gridLayout_set.addLayout(self.gridLayout, 0, 0, 1, 2)
        
        self.buttonBox_set = QtGui.QDialogButtonBox(Psymon_Settings)
        self.buttonBox_set.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_set.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_set.setObjectName(_fromUtf8("buttonBox_set"))
        self.gridLayout_set.addWidget(self.buttonBox_set, 1, 1, 1, 1)
        
        self.pushButton = QtGui.QPushButton(Psymon_Settings)
        self.pushButton.setText(QtGui.QApplication.translate("Psymon_Settings", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_set.addWidget(self.pushButton, 1, 0, 1, 1)

        self.retranslateUi(Psymon_Settings)
        QtCore.QObject.connect(self.buttonBox_set, QtCore.SIGNAL(_fromUtf8("accepted()")), Psymon_Settings.accept)
        QtCore.QObject.connect(self.buttonBox_set, QtCore.SIGNAL(_fromUtf8("rejected()")), Psymon_Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Psymon_Settings)

    def retranslateUi(self, Psymon_Settings):
        pass


