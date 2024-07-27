"""
这里输出去噪后的信号图
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# 设置绘图大小
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class QuzaoPlot:
    def __init__(self, signal, fs, output_path):
        self.signal = signal
        self.fs = fs
        self.output_path = output_path

    def QuzaoPlot(self):
        # 绘制彩色频谱图
        plt.figure(figsize=(10, 6))
        t = np.arange(len(self.signal)) / self.fs

        # 绘制 ECG 信号
        plt.figure(figsize=(12, 6))
        plt.plot(t, self.signal, label='ECG Signal')
        plt.title('心电信号图（ECG）')
        plt.xlabel('时间 (s)')
        plt.ylabel('幅值 (uV)')
        plt.legend()
        plt.grid()
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        base_filename = os.path.join(self.output_path, "ECG")
        file_extension = ".png"
        output_file = base_filename + file_extension
        counter = 1

        while os.path.exists(output_file):
            output_file = f"{base_filename}_{counter}{file_extension}"
            counter += 1
        plt.savefig(output_file)


