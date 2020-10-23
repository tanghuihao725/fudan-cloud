import pandas as pd
import numpy as np
import argparse

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
#from sklearn.externals import joblib
import pickle

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv1D, Dropout
from keras.optimizers import SGD,Adam


parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', type=str, default='./sample_train.txt')
parser.add_argument('--model_name', type=str, default='sample')
parser.add_argument('--feature_length', type=int,default=20)
parser.add_argument('--device_num', type=int,default=10)
parser.add_argument('--material_num', type=int,default=10)
parser.add_argument('--epoch', type=int,default=1)
args = parser.parse_args()

if __name__=="__main__":
    train_dir=args.train_dir

    model_name=args.model_name
    feature_length=args.feature_length
    device_num=args.device_num
    material_num=args.material_num
    
    cols=['feature_'+str(i) for i in range(feature_length)]
    cols.append('time')
    cols.extend(['device_'+str(i) for i in range(device_num)])
    cols.extend(['material_'+str(i) for i in range(material_num)])
    df=pd.read_csv(train_dir,names=cols)
    data=df.iloc[:,:feature_length].values
    data = StandardScaler().fit_transform(data)
    
    time_model = Ridge(alpha=1.0).fit(data, df.iloc[:,feature_length:feature_length+1].values)
    joblib.dump(time_model, model_name+'_time'+'.pkl')
    #with open(model_name+'_time'+'.pkl','wb') as f:
    #    pickle.dump(time_model,f)

    d_m_labels=df.iloc[:,feature_length+1:].values
    data = np.expand_dims(data, axis=2)
    model = Sequential()
    model.add(Conv1D(128,3,activation='relu',input_shape=(feature_length, 1)))
    model.add(Conv1D(64,3))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dropout(0.4))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(device_num+material_num))
    
    #sgd = SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.01),metrics=['accuracy'])
    
    nb_epoch = args.epoch
    model.fit(data, d_m_labels, nb_epoch=nb_epoch, batch_size=128)
    #model.save(model_name+'.h5') 
    model.save_weights(model_name+'.h5') 
