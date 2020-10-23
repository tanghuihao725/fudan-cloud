# coding: UTF-8
import sys
import numpy as np
import pandas as pd


def gra(data, rho):
    # 数据均值化处理
    data_mean = data.mean(axis=0)
    data_pro = data/data_mean

    # create data_pro to excel
    #data_df = pd.DataFrame(data_pro)
    #writer = pd.ExcelWriter('data_pro.xlsx')
    # float_format 控制精度
    #data_df.to_excel(writer, 'sheet1', float_format='%.5f')
    #writer.save()

    # 提取参考队列和比较队列
    ck = data_pro[:, 0]
    bj = data_pro[:, 1:]

    # 求最大差和最小差
    Delta = np.abs(ck.reshape(6,1) - bj)
    mmax = Delta.max()
    mmin = Delta.min()

    # 求关联系数
    ksi = ((mmin + rho * mmax) / (Delta + rho * mmax))
    # 求关联度
    ri = np.mean(ksi, axis=0)
    return ri

import sys, getopt
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'w',encoding='UTF-8')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('python model.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('python model.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('输入的文件为：', inputfile)
   print( '输出的文件为：', outputfile)
   inputfile='equipmentData.txt'
   outputfile='./result/predictResult.txt'
   file = pd.read_csv(inputfile, sep='\t') #'equipmentData.txt'
   #print(file)

   pd1 = file.set_index(['年份'])
   data = np.array(pd1, dtype=np.float64)
   # 分辨系数rho取0.5
   ri = gra(data, 0.5)
   print(ri)
   rr = np.argsort(ri)
   print('最关联的两个设备为：', rr[-1:-3:-1])
   print('这两个设备与生产效率的关联系数为：', ri[rr[-1:-3:-1]])
   with open(outputfile,'w') as f:
       f.write('最关联的两个设备为：\n')
   text_save(outputfile,list(rr[-1:-3:-1]))
   with open(outputfile,'a') as f:
       f.write('这两个设备与生产效率的关联系数为：\n')
   text_save(outputfile,list(ri[rr[-1:-3:-1]]))


#python RelationalAnalysis.py -i ./equipmentData.txt –o ./result/RAResult.txt
if __name__ == "__main__":
   main(sys.argv[1:])
