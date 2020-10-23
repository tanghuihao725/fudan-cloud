import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--db_dir', type=str, default='./sample_db.txt')
parser.add_argument('--search_item_dir', type=str, default='./sample_item.txt')
parser.add_argument('--result_dir', type=str, default='./result/predictResult.txt')
parser.add_argument('--topK', type=int, default=5)
parser.add_argument('--feature_length', type=int,default=20)
parser.add_argument('--device_num', type=int,default=10)
parser.add_argument('--material_num', type=int,default=10)

args = parser.parse_args()

def cosine_similarity(x,y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom
if __name__=="__main__":
    topK=args.topK
    feature_length=args.feature_length
    device_num=args.device_num
    material_num=args.material_num
    db_dir=args.db_dir
    search_item_dir=args.search_item_dir
    result_dir=args.result_dir
    temp=''
    with open(search_item_dir,'r',encoding='UTF-8') as f:
        s=f.readline().replace('\n','').split(',')
        test=np.array([eval(i) for i in s])
        cols=['feature_'+str(i) for i in range(feature_length)]
        cols.append('time')
        cols.extend(['device_'+str(i) for i in range(device_num)])
        cols.extend(['material_'+str(i) for i in range(material_num)])
        df=pd.read_csv(db_dir,names=cols)
        data=df.iloc[:,:feature_length].values
        sim=[cosine_similarity(test,np.array(i)) for i in data]
        result=pd.DataFrame({
            'similarity':sim
        })
        result=pd.concat([result,df.iloc[:,feature_length:]],axis=1)
        result=result.sort_values(by='similarity',ascending=False)
        result=result[:topK]

        for line in result.values:
            temp+='Similarity:'+str(line[0])+'\n'
            temp+='Required '+str(line[1])+' day(s)'+'\n'
            temp+='Required '+' '.join(['device_'+str(i) for i in range(device_num)  if line[2+i]==1] )+'\n'
            temp+='Required '+' '.join(['material_'+str(i) for i in range(material_num) if line[2+device_num+i]==1])+'\n'
            temp+='************************************'+'\n'

        print(temp)
        with open(result_dir,'w',encoding='UTF-8') as f:
            f.write(temp)
