"""
这个文件用来写滤波函数，用于去噪
"""

from PyEMD import EMD
import numpy as np
from scipy import signal
from scipy.signal import iirnotch
import pywt


class Filtration:
    def __init__(self, signal, fs):
        self.signal = signal
        self.fs = fs

    # 用EMD经验模态分析来去掉基线漂移的干扰
    def baseline_drift(self):
        filed_signal = 0
        emd = EMD()  # 实例化EMD
        imfs = emd.emd(self.signal)
        if len(imfs) >= 3:
            np.delete(imfs, -1, axis=1)
        else:
            pass
        for imf in imfs:
            filed_signal += imf
        return filed_signal

    # 用陷波器去除工频干扰
    def powerline_interference(self):
        f0 = 50   # 噪声的中心频率，我国固定为50hz
        Q = 2.0   # 设为2减小边界效应
        b, a = iirnotch(f0, Q, self.fs)
        filtered_signal = signal.lfilter(b, a, self.signal)
        return filtered_signal

    # 小波变换去除肌电干扰
    def myo_interference(self):
        # 选择小波基函数和分解等级
        wavelet = 'db4'
        level = 5
        # 小波分解
        ecg_signal = pywt.wavedec(self.signal, wavelet, level=level)
        # 去除肌电信号干扰
        # 这里去除第 1 到 3 级频带，保留较低频带
        filtered_coeffs = ecg_signal.copy()
        for i in range(1, 4):
            filtered_coeffs[i] = np.zeros_like(ecg_signal[i])
        # 重构滤波后的信号
        filtered_signal = pywt.waverec(filtered_coeffs, wavelet)
        return filtered_signal


