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
    #type trans
    for i in df.columns.values.tolist():
        df[i]=df[i].apply(str)
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
        if len(j)==1 and strDecode[j[0]].endswith('1') :
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
    共有n列
    com_n表示部件n是否故障（0表示未发生故障，1表示发生故障）。
    '''
    support=args.support
    confidence=args.confidence
    train_dir=args.train_dir
    rules_dir=args.rules_dir

    #data,strDecode=data_pre(train_dir)
    data,strDecode=data_pre('trainDataGZ.txt')
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