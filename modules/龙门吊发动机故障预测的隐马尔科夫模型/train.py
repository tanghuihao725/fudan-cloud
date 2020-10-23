'''
从历史数据中训练出模型
'''
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import argparse
from hmmlearn.hmm import GaussianHMM
parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str, default='./trainDataHJ.txt')
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
'''
这个数据集仅供测试模型使用，其中各特征生成方式如下：
门座吊使用时间x(0) 满足均值为5，标准差为1的正态分布
门座吊长度 x(1) 满足最大值10，最小值0.1的均匀分布
门座吊每吊速度 x(2) 满足均值12，标准差3的正态分布
门座吊横截面积 x(3)满足最大值5，最小值1的均匀分布
每吊重量 x(4) 满足均值为500，标准差为100的正态分布
吊数：随机为1-4之间的数
门座吊操作人员的人数x(6) 随机为1-9之间的数
门座吊人员团队的熟练度 随机0-1之间的数
'''
# trainData = np.load(args.train_dir)
trainData = txt_to_numpy(args.train_dir,batch_n,input_data+1)
trainData = torch.tensor(trainData, dtype=torch.float32)
trainData = Variable(trainData, requires_grad=False)
train_x = trainData[:, :8]
import codecs
f = codecs.open(args.train_dir, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取
line = f.readline()   # 以行的形式进行读取文件
train_date = []
while line:
    a = line.split()
    b = a[9:10]   # 这是选取需要读取的位数
    train_date.append(b)  # 将其添加在列表之中
    line = f.readline()
f.close()

print(train_date)
train_y = torch.unsqueeze(trainData[:, 8], 1)
# print(train_x)
# print(train_y)

# 建立神经网络，该网络有两个隐藏层，激活函数使用ReLU()

if __name__ == "__main__":
    # 迭代次数
    train_x = features_init(train_x)
    model = GaussianHMM(n_components=3, covariance_type='diag', n_iter=1000).fit(train_x)
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
    output = open('./model/modelWorkTime_HMMOPS.pth', 'wb')
    s = pickle.dump(model, output)
    output.close()





