import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from UI.states import Ui_main
from function import filtration, HHT, WVD, STFT, CWT
from plot_utils.HHT_plot import HHT_plot
from plot_utils.WVD_plot import WVD_plot
from plot_utils.STFT_plot import STFT_plot
from plot_utils.Quzao_plot import QuzaoPlot
from plot_utils.CWT_plot import CWT_plot
import sys
from select_window import SelectWindow


class MainWindow(QtWidgets.QWidget, Ui_main):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.HHTp.clicked.connect(self.set_processing_method)
        self.WVD.clicked.connect(self.set_processing_method)
        self.STFT.clicked.connect(self.set_processing_method)
        self.WCT.clicked.connect(self.set_processing_method)
        self.quzao.clicked.connect(self.set_processing_method)

        self.lineEdit.mousePressEvent = self.showFileSelectorDialog
        self.lineEdit_2.mousePressEvent = self.showDirectorySelectorDialog

        self.processing_method = None
        self.selected_signal = None  # 用于存储选择窗口返回的信号数据

    def set_processing_method(self):
        sender = self.sender()
        self.processing_method = sender.objectName()
        self.openSelectWindow()

    def showFileSelectorDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "选择输入文件", "", "JSON Files (*.json);;All Files (*)",
                                                   options=options)
        if file_path:
            self.lineEdit.setText(file_path)

    def showDirectorySelectorDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "", options=options)
        if directory:
            self.lineEdit_2.setText(directory)

    def openSelectWindow(self):
        if not self.validate_inputs():
            return

        input_path, _, _ = self.get_input()
        self.select_window = SelectWindow(input_path)
        self.select_window.signal_selected.connect(self.processSelectedSignal)  # 连接信号
        self.select_window.show()

    # def storeSelectedSignal(self, signal):
    #     self.selected_signal = signal  # 存储接收到的信号数据

    def processSelectedSignal(self, signal):
        self.selected_signal = signal  # 存储接收到的信号数据
        print(self.processing_method)
        if self.selected_signal is None:
            print("No signal selected.")
            return
        input_path, _, sampling_frequency = self.get_input()
        fs = float(sampling_frequency)
        print(f"成功获取频率：{sampling_frequency}")
        self.selected_signal = np.array(self.selected_signal)
        if self.processing_method == 'HHTp':
            print(type(self.selected_signal))
            self.handleHHTp(self.selected_signal, fs)
        elif self.processing_method == 'WVD':
            self.handleWVD(self.selected_signal, fs)
        elif self.processing_method == 'STFT':
            self.handleSTFT(self.selected_signal, fs)
        elif self.processing_method == 'WCT':
            self.handleWCT(self.selected_signal, fs)
        elif self.processing_method == 'quzao':
            self.handleQuzao(self.selected_signal, fs)

    def get_input(self):
        input_path = self.lineEdit.text().strip()
        output_path = self.lineEdit_2.text().strip()
        sampling_frequency = self.fs.text().strip()
        return input_path, output_path, sampling_frequency

    def validate_inputs(self):
        input_path, output_path, sampling_frequency = self.get_input()
        if not input_path:
            self.show_message("输入错误", "请输入有效的信号文件路径。")
            return False
        if not output_path:
            self.show_message("输入错误", "请选择有效的输出文件夹。")
            return False
        if not sampling_frequency or not sampling_frequency.replace('.', '', 1).isdigit():
            self.show_message("输入错误", "请输入有效的采样频率。")
            return False
        return True

    def handleHHTp(self, signal, fs):
        filtration_object1 = filtration.Filtration(signal=signal, fs=fs)
        clean_signal1 = filtration_object1.baseline_drift()
        filtration_object2 = filtration.Filtration(signal=clean_signal1, fs=fs)
        clean_signal2 = filtration_object2.powerline_interference()
        filtration_object3 = filtration.Filtration(signal=clean_signal2, fs=fs)
        clean_signal = filtration_object3.myo_interference()
        hhtp = HHT.HHT(signal=clean_signal, fs=fs)
        frequencies, times, Sxx = hhtp.hht()
        plot = HHT_plot(frequencies=frequencies, times=times, Sxx=Sxx, output_path=self.get_input()[1])
        plot.HHT_plot()  # 调用类的方法来生成图像

    def handleWVD(self, signal, fs):
        # print("WVD")  # 占位检测功能健全
        filtration_object1 = filtration.Filtration(signal=signal, fs=fs)
        clean_signal1 = filtration_object1.baseline_drift()
        filtration_object2 = filtration.Filtration(signal=clean_signal1, fs=fs)
        clean_signal2 = filtration_object2.powerline_interference()
        filtration_object3 = filtration.Filtration(signal=clean_signal2, fs=fs)
        clean_signal = filtration_object3.myo_interference()
        wvd = WVD.WVD(signal=clean_signal)
        # print(type(self.get_input()[2]))
        fs = int(self.get_input()[2])
        tfr, t, f = wvd.WVD()
        plot = WVD_plot(tfr=tfr, t=t, f=f, fs=fs, output_path=self.get_input()[1])
        plot.WVD_plot()

    def handleSTFT(self, signal, fs):
        filtration_object1 = filtration.Filtration(signal=signal, fs=fs)
        clean_signal1 = filtration_object1.baseline_drift()
        filtration_object2 = filtration.Filtration(signal=clean_signal1, fs=fs)
        clean_signal2 = filtration_object2.powerline_interference()
        filtration_object3 = filtration.Filtration(signal=clean_signal2, fs=fs)
        clean_signal = filtration_object3.myo_interference()
        fs = int(self.get_input()[2])
        stft = STFT.STFT(signal=clean_signal, fs=fs)
        frequencies, times, Zxx = stft.stft_use()
        plot = STFT_plot(frequencies=frequencies, times=times, Zxx=Zxx, output_path=self.get_input()[1])
        plot.STFT_plot()

    def handleWCT(self, signal, fs):
        filtration_object1 = filtration.Filtration(signal=signal, fs=fs)
        clean_signal1 = filtration_object1.baseline_drift()
        filtration_object2 = filtration.Filtration(signal=clean_signal1, fs=fs)
        clean_signal2 = filtration_object2.powerline_interference()
        filtration_object3 = filtration.Filtration(signal=clean_signal2, fs=fs)
        clean_signal = filtration_object3.myo_interference()
        fs = int(self.get_input()[2])
        cwt = CWT.CWT(signal=clean_signal, fs=fs)
        coefficients, frequencies = cwt.cwt()
        plot = CWT_plot(frequencies=frequencies, coefficients=coefficients, output_path=self.get_input()[1],
                        signal=clean_signal, fs=fs)
        plot.CWT_plot()

    def handleQuzao(self, signal, fs):
        # print("WVD")  # 占位检测功能健全
        filtration_object1 = filtration.Filtration(signal=signal, fs=fs)
        clean_signal1 = filtration_object1.baseline_drift()
        filtration_object2 = filtration.Filtration(signal=clean_signal1, fs=fs)
        clean_signal2 = filtration_object2.powerline_interference()
        filtration_object3 = filtration.Filtration(signal=clean_signal2, fs=fs)
        clean_signal = filtration_object3.myo_interference()
        fs = int(self.get_input()[2])
        plot = QuzaoPlot(signal=clean_signal, fs=fs, output_path=self.get_input()[1])
        plot.QuzaoPlot()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
