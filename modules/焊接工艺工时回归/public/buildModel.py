import torch

# 输入焊接工时和相关特征的数据量
NUM_SAMPLES = 2000
# 隐藏层1的节点数
HIDDEN1 = 100
# 隐藏层2的节点数
HIDDEN2 = 50
# 相关特征个数
INPUTSIZE = 9
# 神经网络输出层的节点数
OUTPUTSIZE = 1


# 建立神经网络，该网络有两个隐藏层，激活函数使用ReLU()
class model(torch.nn.Module):
    def __init__(self, INPUTSIZE, OUTPUTSIZE, HIDDEN1, HIDDEN2):
        super(model, self).__init__()
        self.regression = torch.nn.Sequential(
            torch.nn.Linear(INPUTSIZE, HIDDEN1),
            torch.nn.ReLU(),
            torch.nn.Linear(HIDDEN1, HIDDEN2),
            torch.nn.ReLU(),
            torch.nn.Linear(HIDDEN2, OUTPUTSIZE)
        )

    def forward(self, x):
        x = self.regression(x)
        return x
