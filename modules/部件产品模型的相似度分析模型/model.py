import pandas as pd
import numpy as np


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--db_dir', type=str, default='./sample_db.txt')
parser.add_argument('--test_dir', type=str, default='./sample_test.txt')
parser.add_argument('--result_dir', type=str, default='./result/predictResult.txt')
parser.add_argument('--topK', type=int, default=20)
args = parser.parse_args()

def cosine_similarity(x,y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom
if __name__ == "__main__":
    k=args.topK
    db_dir=args.db_dir
    test_dir=args.test_dir
    result_dir=args.result_dir
    with open(test_dir,'r',encoding='UTF-8') as f:
        s=f.readline().replace('\n','').split(',')
        name=s[0]
        test=np.array([eval(i) for i in s[1:]])
        df=pd.read_csv(db_dir)
        data=df.iloc[:,1:].values
        sim=[cosine_similarity(test,np.array(i)) for i in data]
        result=pd.DataFrame({
            'name':df.iloc[:,0],
            'similarity':sim
        })
        result=result.sort_values(by='similarity',ascending=False)
        result=result[:k]
        print(result)
        result.to_csv(result_dir,index=False)