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
    df['born']=df['born'].map(lambda x:now_y-x+1)
    df['start_work']=df['start_work'].map(lambda x:now_y-x+1)
    #iscretization
    bins=[18,25,35,45,60]
    df['born']=pd.cut(df['born'],bins,right=False,labels=['1','2','3','4'])
    bins=[1,3,5,10,41]
    df['start_work']=pd.cut(df['start_work'],bins,right=False,labels=['1','2','3','4'])
    bins=[0,0.6,0.8,0.9,1]
    df['prof']=pd.cut(df['prof'],bins,right=False,labels=['1','2','3','4'])
    #type trans
    df['dept']=df['dept'].apply(str)
    df['mach_cat']=df['mach_cat'].apply(str)
    df['meth_cat']=df['meth_cat'].apply(str)
    df['degree']=df['degree'].apply(str)
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
    born表示操作人员出生年份,
    start_work表示操作人员入职年份,
    dept表示操作人员所属部门编号,
    degree表示操作人员学历（初中、高中、专科、本科以上，可用1，2，3，4表示），
    meth_cat表示下料工艺种类（可用一个整数表示） 
    prof表示操作人员的熟练度（一个0-1之间的数，越大表明这个操作人员工作效率越高）。
    mach_cat表示下料机型号（可用一个整数表示）
    time表示完成此次焊接所需的耗时（短、较短、一般、较长、长，可用1，2，3，4，5表示）。

    '''
    support=args.support
    confidence=args.confidence
    train_dir=args.train_dir
    rules_dir=args.rules_dir

    #data,strDecode=data_pre(train_dir)
    data,strDecode=data_pre('trainDataXL.txt')
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