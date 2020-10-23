import pandas as pd
import numpy as np
import argparse

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
#from sklearn.externals import joblib
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv1D, Dropout
from keras.models import load_model

parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', type=str, default='./sample_test.txt')
parser.add_argument('--result_dir', type=str, default='./result/predictResult.txt')
parser.add_argument('--time_model_dir', type=str, default='./sample_time.pkl')
parser.add_argument('--model_dir', type=str, default='./sample_model.h5')
parser.add_argument('--feature_length', type=int,default=20)
parser.add_argument('--device_num', type=int,default=10)
parser.add_argument('--material_num', type=int,default=10)

args = parser.parse_args()

def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s

if __name__=="__main__":
    test_dir=args.test_dir
    result_dir=args.result_dir
    feature_length=args.feature_length
    device_num=args.device_num
    material_num=args.material_num
    time_model_dir=args.time_model_dir
    model_dir=args.model_dir
    
    cols=['feature_'+str(i) for i in range(feature_length)]
    df=pd.read_csv(test_dir,names=cols)
    data=df.values
    data=StandardScaler().fit_transform(data) 
    #with open(time_model_dir,'rb') as f:
    #    time_model=pickle.load(f)
    time_model=joblib.load(time_model_dir)
    time=time_model.predict(data)
    time=[i[0] for i in time]

    data=np.expand_dims(data, axis=2)
    model=load_model(model_dir)
    result=model.predict(data)
    result=sigmoid(result)
    result[result<0.5]=0
    result[result>0.5]=1

    temp=''
    for (t,d) in zip(time,result.tolist()):
        temp+='Need '+str(t)+' day(s)\n'
        temp+='Require '+' '.join(['device_'+str(i) for i in range(device_num) if d[i]==1])+'\n'
        temp+='Require '+' '.join(['material_'+str(i) for i in range(material_num) if d[device_num+i]==1])+'\n'
        temp+='******************\n'

    with open(result_dir,'w',encoding='UTF-8') as f:
        f.write(temp)
    print(temp)