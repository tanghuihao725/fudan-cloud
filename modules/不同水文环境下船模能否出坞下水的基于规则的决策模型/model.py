# coding:utf-8
import sys, getopt,os
import pandas as pd

from sklearn import tree
from sklearn.datasets import load_iris

from math import log
import operator
#reload(sys)
#sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'w',encoding='UTF-8')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")
if __name__ == '__main__':
    trainfile = ''
    testfile = ''
    outputfile = ''
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "ha:b:o:", ["trfile=", "tefile=","ofile="])
    except getopt.GetoptError:
        print('python model.py -a <trainfile> -b <testfile>  -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python model.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-a", "--trfile"):
            trainfile = arg
        elif opt in ("-b", "--tefile"):
            testfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    #print('输入的文件为：', trainfile,testfile)
    #print('输出的文件为：', outputfile)
    trainfile='environmentDat.txt'
    testfile='environmentTestDat.txt'
    outputfile='./result/predictResult.txt'
    iris_test = pd.read_csv(testfile)

    iris_train = pd.read_csv(trainfile)
    labels_iris_tr = iris_train.pop('labels_iris')
    labels_iris_te = iris_test.pop('labels_iris')

    dt = tree.DecisionTreeClassifier()
    dt.fit(iris_train,labels_iris_tr)
    #score = dt.score(iris_test,labels_iris_te)
    #print("预测在测试集上的得分为：",score)

    predict =  dt.predict(iris_test)
    print("船坞是否能下水的预测结果为：", predict)
    with open(outputfile, 'w') as f:
        f.write('船坞是否能下水的预测结果为：\n')
    text_save(outputfile, list(predict))

