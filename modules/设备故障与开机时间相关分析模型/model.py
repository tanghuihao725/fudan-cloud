from cca import CCA
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str, default='./input.txt')
args = parser.parse_args()

filename = args.train_dir
dataset = []
with open(filename, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = list(line.strip().split())
        for item in line:
            item = item.split('_')
            s = []
            for val in item:
                s.append(float(val))
            dataset.append(s)

train_data = pd.DataFrame(dataset)
train_data.columns = ["intensity", "last", "time", "status"]

data = train_data.values

intensity = data[:, 0]
last = data[:, 1]

status = data[:, 2:]

intensity = intensity.reshape(-1, 1)
last = last.reshape(-1, 1)

res = []

cca = CCA()
cca.fit(intensity, status)
cca.transform(intensity, status)
cca.ptransform(intensity, status)
col = cca.calc_correlations()
res.append(col)

cca.fit(last, status)
cca.transform(last, status)
cca.ptransform(last, status)
col = cca.calc_correlations()
res.append(col)

with  open('./result/predictResult.txt', 'w',encoding='UTF-8') as f:
    s = ''
    x = res[0]
    y = res[1]
    if x > 0.6 or x < -0.6:
        s += '设备使用时长与设备故障有关\n'
    else:
        s += '设备使用时长与设备故障无关\n'
    if y > 0.6 or y < -0.6:
        s += '作业区场地与设备故障有关\n'
    else:
        s += '作业区场地与设备故障无关\n'
    f.write(s)