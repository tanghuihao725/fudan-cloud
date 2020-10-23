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
    bins=[0,2,5,11]
    df['d_age']=pd.cut(df['d_age'],bins,right=False,labels=['1','2','3'])
    bins=[0,2,5,11]
    df['busy_time']=pd.cut(df['busy_time'],bins,right=False,labels=['1','2','3'])
    bins=[0,2,5,11]
    df['free_time']=pd.cut(df['free_time'],bins,right=False,labels=['1','2','3'])
    #type trans
    df['on_time']=df['on_time'].apply(str)
    df['start_time_type']=df['start_time_type'].apply(str)
    df['close_time_type']=df['close_time_type'].apply(str)
    df['d_type']=df['d_type'].apply(str)
    df['is_fault']=df['is_fault'].apply(str)
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
        if len(j)==1 and strDecode[j[0]].startswith('is_fault') :
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
    on_time表示开机时间长短（1表示短，2表示长，3表示超长）,
    start_time_type表示开机时段（有1-8 八个时段）
    close_time_type表示关机时段（有1-8 八个时段）
    busy_time表示设备处于繁忙阶段的次数
    free_time表示设备处于空闲阶段的次数
    d_type表示设备类别（可用一个整数表示）
    d_age表示设备寿命（可用一个整数表示）
    is_fault表示是否故障（0表示无故障，1表示故障）。

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