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
    now_y=datetime.datetime.now().year
    #transform date to time
    df['ave_born']=df['ave_born'].map(lambda x:now_y-x+1)
    df['ave_start_work']=df['ave_start_work'].map(lambda x:now_y-x+1)
    #iscretization
    bins=[18,25,35,45,60]
    df['ave_born']=pd.cut(df['ave_born'],bins,right=False,labels=['1','2','3','4'])
    bins=[1,3,5,10,41]
    df['ave_start_work']=pd.cut(df['ave_start_work'],bins,right=False,labels=['1','2','3','4'])
    bins=[0,0.6,0.8,0.9,1]
    df['ave_prof']=pd.cut(df['ave_prof'],bins,right=False,labels=['1','2','3','4'])
    bins=[0,10,20,31]
    df['dept_num']=pd.cut(df['dept_num'],bins,right=False,labels=['1','2','3'])
    bins=[0,6,16,26,30]
    df['dept_worker_num']=pd.cut(df['dept_worker_num'],bins,right=False,labels=['1','2','3','4'])
    
    #type trans
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

if __name__=="__main__":
    '''
    数据解释
    ave_born表示班组平均出生年份,
    ave_start_work表示班组平均入职年份,
    dept_num表示班组人数,
    dept_{worker_num表示班组工人数目，
    meth_cat表示焊接工艺种类（可用一个整数表示） 
    ave_prof表示班组平均的熟练度（一个0-1之间的数，越大表明这个操作人员工作效率越高）。
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
    file=open(rules_dir,'w',encoding='UTF-8')
    print('Rules'+'\t'+'support'+'\t'+'confidence'+'\n')
    file.write('Rules'+'\t'+'support'+'\t'+'confidence'+'\n')
    for line in printRules:
        s='\t'.join([str(i) for i in line])
        print(s+'\n')
        file.write(s+'\n')
    file.close()