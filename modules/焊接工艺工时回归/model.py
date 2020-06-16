'''
利用训练好的模型，输入相关参数，预测船厂耗电量
'''
import torch
import argparse
from public.buildModel import model, NUM_SAMPLES
from public.buildModel import HIDDEN1, HIDDEN2, INPUTSIZE, OUTPUTSIZE
from public.utils import txt_to_numpy

parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str,
                    default='./trainDataHJ.txt')
parser.add_argument('--predict_data', type=str, default='./predictData.txt')
args = parser.parse_args()


# 根据历史数据归一化
def features_init(x):
    x[0] = x[0]
    x[1] = x[1]
    x[2] = x[2]
    x[3] = x[3]
    x[4] = x[4]
    x[5] = x[5]
    x[6] = x[6]
    x[7] = x[7]
    x[8] = x[8]
    return x


def maxMinNor(a, i):
    max = torch.max(train_x[:, i])
    min = torch.min(train_x[:, i])
    return (a - min) / float((max - min))


def zNorm(a, i):
    mean = torch.mean(train_x[:, i])
    std = torch.std(train_x[:, i])
    return (a - mean) / std


if __name__ == "__main__":
    predictData = txt_to_numpy(args.predict_data, 1, INPUTSIZE).squeeze()
    test_x = torch.FloatTensor(predictData)

    trainData = txt_to_numpy(args.train_dir, NUM_SAMPLES, INPUTSIZE + 1)
    trainData = torch.tensor(trainData, dtype=torch.float32)
    train_x = trainData[:, :INPUTSIZE]

    model = model(INPUTSIZE=INPUTSIZE,
                  OUTPUTSIZE=OUTPUTSIZE,
                  HIDDEN1=HIDDEN1,
                  HIDDEN2=HIDDEN2)
    # 载入在train中保存的模型
    with torch.no_grad():
        model.load_state_dict(torch.load(
            "./model/modelWorkTime_Welding.pth", map_location='cpu'))
        test_x = features_init(test_x)
        pred_y = model(test_x).item()

    # corr = abs(pred_y - test_y) / test_y

    print("预测工时:{}".format(str(round(pred_y, 2))))
    with open('./result/predictResult.txt', 'w') as f:
        f.write('Working Time is ' + str(round(pred_y, 2)) + '\n')
