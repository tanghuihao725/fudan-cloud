import numpy as np
import pandas as pd
import orangecontrib.associate.fpgrowth as oaf
import datetime
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str, default='./predictData.txt')
parser.add_argument('--rules_dir', type=str, default='./result/predictResult.txt')
parser.add_argument('--support', type=float, default=0.05)
parser.add_argument('--confidence',type=float,default=0.2)
args = parser.parse_args()


def data_pre(path):
    df=pd.read_csv(path)
    #iscretization
    bins=[0,50,70,90,100]
    df['hum']=pd.cut(df['hum'],bins,right=False,labels=['1','2','3','4'])
    bins=[-50.0,-20.0,-10.0,0,10.0,20.0,30.0,41.0]
    df['tem']=pd.cut(df['tem'],bins,right=False,labels=['1','2','3','4','5','6','7'])
    bins=[0,20,100]
    df['per_con']=pd.cut(df['per_con'],bins,right=False,labels=['1','2'])
    #type trans
    df['is_gas']=df['is_gas'].apply(str)
    df['is_metal']=df['is_metal'].apply(str)
    df['mach_cat']=df['mach_cat'].apply(str)
    df['meth_cat']=df['meth_cat'].apply(str)
    df['time']=df['time'].apply(str)
    #one_hot
    df=pd.get_dummies(df)
    strDecode=df.columns.values.tolist()
    data=df.values
    data.dtype=bool
    return data,strDecode

def model(data,support=0.05,confidence=0.2):
    fre_ite=dict(oaf.frequent_itemsets(data,support))  #这里设置置信度
    rules = oaf.association_rules(fre_ite,confidence)
    result=list(rules)
    return result


def dealResult(rules,strDecode):
    returnRules = []
    for i in rules:
        j= list(i[1])
        if len(j)==1 and strDecode[j[0]].startswith('time') :
            temStr = []
            temp=''
            for k in i[0]:
                temp = temp+strDecode[k]+'&'
            temp = temp[:-1]
            temp = temp + ' ==> '
            temp = temp +strDecode[j[0]] 
            temStr.append(temp)
            temStr.append(i[2])
            temStr.append(i[3])
            returnRules.append(temStr)
    returnRules=list(sorted(returnRules,key=lambda x:(-x[2],-x[1])))
    return returnRules
    




if __name__ == "__main__":
    '''
    数据解释
    hum表示湿度,
    tem表示温度,
    is_gas表示焊接作业现场是否存在腐蚀性气体、煤气、蒸气或导电粉尘,
    per_con表示焊接作业现场地面金属导电物质占有系数,
    is_metal表示是否在金属管道、容器内和金属结构内焊接
    meth_cat表示焊接工艺种类（可用一个整数表示） 
    mach_cat表示焊机型号（可用一个整数表示）
    time表示完成此次焊接所需的耗时（短、较短、一般、较长、长，可用1，2，3，4，5表示）。

    '''
    support=args.support
    confidence=args.confidence
    train_dir=args.train_dir
    rules_dir=args.rules_dir

    #data,strDecode=data_pre(train_dir)
    data,strDecode=data_pre('trainDataHJ.txt')
    result=model(data,support,confidence)
    printRules= dealResult(result,strDecode)
    
    #save and print
    file=open(rules_dir,'w',encoding='UTF-8')
    print('Rules'+'\t'+'support'+'\t'+'confidence'+'\n')
    file.write('Rules'+'\t'+'support'+'\t'+'confidence'+'\n')
    for line in printRules:
        s='\t'.join([str(i) for i in line])
        print(s+'\n')
        file.write(s+'\n')
    file.close()