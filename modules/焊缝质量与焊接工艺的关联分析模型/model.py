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
    bins=[0,2,4,6,8,10]
    df['area']=pd.cut(df['area'],bins,right=False,labels=['1','2','3','4','5'])
    bins=[0,2,4,6,8,10]
    df['length']=pd.cut(df['length'],bins,right=False,labels=['1','2','3','4','5'])
    bins=[0,10,12,14,22]
    df['speed']=pd.cut(df['speed'],bins,right=False,labels=['1','2','3','4'])
    bins=[0,2,3,4,5]
    df['cross_area']=pd.cut(df['cross_area'],bins,right=False,labels=['1','2','3','4'])
    bins=[0,450,500,600,800]
    df['shc']=pd.cut(df['shc'],bins,right=False,labels=['1','2','3','4'])
    #type trans
    df['loc']=df['loc'].apply(int).apply(str)
    df['mach_cat']=df['mach_cat'].apply(str)
    df['meth_cat']=df['meth_cat'].apply(str)
    df['quality']=df['quality'].apply(str)
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
        if len(j)==1 and strDecode[j[0]].startswith('quality') :
            temStr = [];
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
    area表示焊缝面积（㎡）
    length表示焊缝长度（m）
    speed表示焊条的融化速度 (m/min),
    cross_area表示焊条的横截面积 (cm^2),
    shc表示焊条的比热容 (J/(kg·K)),
    loc表示焊接位置 (平焊、立焊、横焊和仰焊等，可用1、2、3、4表示),
    meth_cat表示焊接工艺种类（可用一个整数表示）, 
    mach_cat表示焊机型号（可用一个整数表示）,
    quality表示焊缝质量（好、较好、一般、较差、差，可用1，2，3，4，5表示）。

    '''
    support=args.support
    confidence=args.confidence
    train_dir=args.train_dir
    rules_dir=args.rules_dir

    #data,strDecode=data_pre(train_dir)
    data,strDecode=data_pre('trainDataHF.txt')
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