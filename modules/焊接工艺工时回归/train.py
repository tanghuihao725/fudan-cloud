'''
从历史数据中训练出模型
'''
import torch
from sklearn.model_selection import train_test_split
import argparse
from public.buildModel import model, NUM_SAMPLES
from public.buildModel import HIDDEN1, HIDDEN2, INPUTSIZE, OUTPUTSIZE
from public.utils import txt_to_numpy, train, evaluate, load_data

parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str,
                    default='./trainDataHJ.txt')
args = parser.parse_args()

BATCH_SIZE = 64
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
INF = float("inf")


# 参数初始化,将x中的每一个特征进行归一化
def features_init(x):
    x[:, 0] = x[:, 0]
    x[:, 1] = x[:, 1]
    x[:, 2] = x[:, 2]
    x[:, 3] = x[:, 3]
    x[:, 4] = x[:, 4]
    x[:, 5] = x[:, 5]
    x[:, 6] = x[:, 6]
    x[:, 7] = x[:, 7]
    x[:, 8] = x[:, 8]
    return x


def maxMinNor(a):
    max = torch.max(a)
    min = torch.min(a)
    return (a - min) / float((max - min))


def zNorm(a):
    mean = torch.mean(a)
    std = torch.std(a)
    return (a - mean) / std


# 载入历史数据集
trainData = txt_to_numpy(args.train_dir, NUM_SAMPLES, INPUTSIZE + 1)
X = trainData[:, :INPUTSIZE]
Y = trainData[:, INPUTSIZE]

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, train_size=.8, test_size=.2)
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
Y_train = torch.tensor(Y_train, dtype=torch.float32).unsqueeze(1)
Y_test = torch.tensor(Y_test, dtype=torch.float32).unsqueeze(1)
X_train, X_test = features_init(X_train), features_init(X_test)

loader_train = load_data(X_train, Y_train, BATCH_SIZE)
loader_test = load_data(X_test, Y_test, BATCH_SIZE)


if __name__ == "__main__":
    # 迭代次数
    EPOCH_N = 50
    # 加载模型，并定义神经网络各层节点数
    model = model(INPUTSIZE=INPUTSIZE,
                  OUTPUTSIZE=OUTPUTSIZE,
                  HIDDEN1=HIDDEN1,
                  HIDDEN2=HIDDEN2)
    model = model.to(DEVICE)
    # 定义损失函数，这里用损失均方误差
    loss_func = torch.nn.MSELoss().to(DEVICE)
    # 定义优化方法，这里使用Adam
    optimizer = torch.optim.Adam(
        model.parameters(), lr=0.0001, weight_decay=0.005)
    
    # model.load_state_dict(torch.load(
    #     "./model/modelForElectricityCost.pth"))

    best_loss = INF
    for epoch in range(EPOCH_N):
        train_loss = train(model, loader_train, optimizer, loss_func, DEVICE)
        valid_loss = evaluate(model, loader_test, loss_func, DEVICE)
        print("Epoch", epoch, "Train Loss", train_loss)
        print("Epoch", epoch, "Valid Loss", valid_loss)
        if valid_loss < best_loss:
            best_loss = valid_loss
            torch.save(model.state_dict(),
                       './model/modelWorkTime_Welding.pth')
            print("model saved OK")

    print("Train OK")
