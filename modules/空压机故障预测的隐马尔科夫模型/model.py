'''
利用训练好的模型，输入新的焊接相关数据，预测进行焊接的工时
'''
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import argparse
from hmmlearn.hmm import GaussianHMM
parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str, default='./trainDataHJ.txt')
parser.add_argument('--predict_data', type=str, default='./predictData.txt')
args = parser.parse_args()

# 输入焊接历史数据的数据量
batch_n = 1000
# 隐藏层1的节点数
hidden_layer1 = 100
# 隐藏层2的节点数
hidden_layer2 = 20
# 焊接历史数据的参数个数
input_data = 9
# 神经网络输出层的节点数
output_data = 1


def features_init(x):
    x[:, 0] = maxMinNor(x[:, 0])
    x[:, 1] = maxMinNor(x[:, 1])
    x[:, 2] = zNorm(x[:, 2])
    x[:, 3] = zNorm(x[:, 3])
    x[:, 4] = maxMinNor(x[:, 4])
    x[:, 5] = x[:, 5] / 4
    x[:, 6] = maxMinNor(x[:, 6])
    x[:, 7] = x[:, 7]
    return x

def maxMinNor(a):
    max = torch.max(a)
    min = torch.min(a)
    return (a-min)/float((max-min))
def zNorm(a):
    mean = torch.mean(a)
    std = torch.std(a)
    return (a-mean)/std
def txt_to_numpy(filename, row, colu):
    """
	filename:是txt文件路径
	row:txt文件中数组的行数
	colu:txt文件中数组的列数
	"""
    file = open (filename)
    lines = file.readlines()
    # print(lines)
	# 初始化datamat
    datamat = np.zeros((row, colu))

    row_count = 0

    for line in lines:
    	# 写入datamat
        line = line.strip().split(' ')
        datamat[row_count,:] = line[:]
        row_count += 1
    return datamat

# 载入历史数据集
# trainData = np.load(args.train_dir)
trainData = txt_to_numpy(args.predict_data,1,input_data+1)
trainData = torch.tensor(trainData, dtype=torch.float32)
trainData = Variable(trainData, requires_grad=False)
train_x = trainData[:, :8]
import codecs
f = codecs.open(args.predict_data, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取
line = f.readline()   # 以行的形式进行读取文件
train_date = []
while line:
    a = line.split()
    b = a[9:10]   # 这是选取需要读取的位数
    train_date.append(b)  # 将其添加在列表之中
    line = f.readline()
f.close()

train_y = torch.unsqueeze(trainData[:, 8], 1)
# print(train_x)
# print(train_y)

# 建立神经网络，该网络有两个隐藏层，激活函数使用ReLU()

if __name__ == "__main__":

    # import pickle
    # output = open('./model/modelWorkTime_HMMOPS.pth', 'wb')
    # s = pickle.dump(model, output)
    # output.close()

    # test_x = Variable(torch.FloatTensor(predictData))
    # # 为了归一化测试数据，需要载入历史数据
    # trainData = txt_to_numpy(args.train_dir, batch_n, input_data + 1)
    # # trainData = np.load(args.train_dir)
    # trainData = torch.tensor(trainData, dtype=torch.float32)
    # trainData = Variable(trainData, requires_grad=False)
    # train_x = trainData[:, :8]
    # import pickle
    #
    # input = open("./model/modelWorkTime_HMMOPS.pth", 'rb')
    # model = pickle.load(input)
    # input.close()
    # test_x = features_init(test_x)
    #
    # print(model.predict(test_x))

    import pickle

    input = open('./model/modelWorkTime_HMMOPS.pth', 'rb')
    model = pickle.load(input)
    print(model.predict(train_x))
    result = txt_to_numpy(args.predict_data, 1, input_data+1 )
    result_x = result[:, :9]
    f = open('./result/predictResult.txt', 'w',encoding='UTF-8')
    if (model.predict(train_x)) == 0:
        f.write('故障发生情况是 '+"否"+'\n')
    elif (model.predict(train_x)) == 1:
        f.write('故障发生情况是 '+"有可能"+'\n')
    else:
        f.write('故障发生情况是 '+"是"+ '\n')

    f.close()
