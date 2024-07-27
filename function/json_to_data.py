"""
在这里将json文件中的数据提取成易于处理的数据类型
"""

import json
import os
import numpy as np

class JsonToData:
    def __init__(self, json_file, idx):
        self.json_file = json_file
        self.idx = idx
        self.data = {}

    def json_to_data_all(self, json_file):
        with open(json_file, 'r') as f:
            print(json_file)
            self.data = json.load(f)
            # for key, value in data.items():
            #     for key1, value1 in value.items():
            #         print(key1)
            """
            通过注释的代码，我了解到这个json文件的格式以及有用信息储存位置
            """
            real_data_all = self.data['data']
            keys = list(real_data_all.keys())  # 把键字典转化成列表，其中的每个元素这将成为每一幅图的序号
            cnt = 0
            for key in keys:
                cnt += 1
                Y = real_data_all[key]
                Y = Y.split(' ')
                Y_num = []
                for i in Y:
                    i = int(i)
                    i = np.float64(i)
                    Y_num.append(i)
                real_data_all[key] = np.array(Y_num)
            # 返回十二导联图的全部数据，其格式仍然是字典
            return real_data_all

    def data_slected(self, json_file, idx):   # 获取十二导联中的某个信号数据
        data_all = JsonToData.json_to_data_all(self, json_file)   # 拿到全部数据
        return data_all[idx]   # 通过键来获取值
