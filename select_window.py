from PyQt5 import QtWidgets
from UI.select_signal_window import Ui_Form
from PyQt5.QtWidgets import QFileDialog
from function import json_to_data
from PyQt5.QtCore import pyqtSignal


class SelectWindow(QtWidgets.QWidget, Ui_Form):
    signal_selected = pyqtSignal(object)  # 定义一个自定义信号，传递信号数据

    def __init__(self, input_path, parent=None):
        super(SelectWindow, self).__init__(parent)
        self.setupUi(self)
        self.input_path = input_path

        # 连接按钮事件
        self.I.clicked.connect(self.I_clicked)
        self.II.clicked.connect(self.II_clicked)
        self.III.clicked.connect(self.III_clicked)
        self.AVR.clicked.connect(self.AVR_clicked)
        self.AVL.clicked.connect(self.AVL_clicked)
        self.AVF.clicked.connect(self.AVF_clicked)
        self.V1.clicked.connect(self.V1_clicked)
        self.V2.clicked.connect(self.V2_clicked)
        self.V3.clicked.connect(self.V3_clicked)
        self.V4.clicked.connect(self.V4_clicked)
        self.V5.clicked.connect(self.V5.clicked)
        self.V6.clicked.connect(self.V6.clicked)
        self.all.clicked.connect(self.all_clicked)

    def I_clicked(self):
        signal_I = json_to_data.JsonToData(self, idx='I').data_slected(self.input_path, idx='I')
        self.return_signal(signal_I)

    def II_clicked(self):
        signal_II = json_to_data.JsonToData(self, idx='II').data_slected(self.input_path, idx='II')
        self.return_signal(signal_II)

    def III_clicked(self):
        signal_III = json_to_data.JsonToData(self, idx='III').data_slected(self.input_path, idx='III')
        self.return_signal(signal_III)

    def AVR_clicked(self):
        signal_AVR = json_to_data.JsonToData(self, idx='AVR').data_slected(self.input_path, idx='AVR')
        self.return_signal(signal_AVR)

    def AVL_clicked(self):
        signal_AVL = json_to_data.JsonToData(self, idx='AVL').data_slected(self.input_path, idx='AVL')
        self.return_signal(signal_AVL)

    def AVF_clicked(self):
        signal_AVF = json_to_data.JsonToData(self, idx='AVF').data_slected(self.input_path, idx='AVF')
        self.return_signal(signal_AVF)

    def V1_clicked(self):
        signal_V1 = json_to_data.JsonToData(self, idx='V1').data_slected(self.input_path, idx='V1')
        self.return_signal(signal_V1)

    def V2_clicked(self):
        signal_V2 = json_to_data.JsonToData(self, idx='V2').data_slected(self.input_path, idx='V2')
        self.return_signal(signal_V2)

    def V3_clicked(self):
        signal_V3 = json_to_data.JsonToData(self, idx='V3').data_slected(self.input_path, idx='V3')
        self.return_signal(signal_V3)

    def V4_clicked(self):
        signal_V4 = json_to_data.JsonToData(self, idx='V4').data_slected(self.input_path, idx='V4')
        self.return_signal(signal_V4)

    def V5_clicked(self):
        signal_V5 = json_to_data.JsonToData(self, idx='V5').data_slected(self.input_path, idx='V5')
        self.return_signal(signal_V5)

    def V6_clicked(self):
        signal_V6 = json_to_data.JsonToData(self, idx='V6').data_slected(self.input_path, idx='V6')
        self.return_signal(signal_V6)

    def all_clicked(self):
        # all_signal = json_to_data.JsonToData(self, idx=None).json_to_data_all(self.input_path)
        # self.return_signal(all_signal)
        self.I_clicked()
        self.II_clicked()
        self.III_clicked()
        self.AVR_clicked()
        self.AVL_clicked()
        self.AVF_clicked()
        self.V1_clicked()
        self.V2_clicked()
        self.V3_clicked()
        self.V4_clicked()
        self.V5_clicked()
        self.V6_clicked()

    def return_signal(self, signal):
        self.signal_selected.emit(signal)
        self.close()
        print("success")

    def showFileSelectorDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "选择输入文件", "", "JSON Files (*.json);;All Files (*)",
                                                   options=options)
        if file_path:
            self.window.lineEdit.setText(file_path)

    def showDirectorySelectorDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "", options=options)
        if directory:
            self.window.lineEdit_2.setText(directory)
