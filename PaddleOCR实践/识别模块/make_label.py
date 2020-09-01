# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:53:31 2020

@author: jkh
"""
import os

specific_symbol = {':':'冒','*':'星','?':'问','"':'引','<':'左尖','>':'右尖','|':'竖','\\':'左斜',r'/':'右斜'}

def write_txt(txt_path,img_path):
    with open(txt_path,'w') as f:   
        img_name = []
        labels = []
        img_path = img_path
        for root,sub,files in os.walk(img_path):
            for file in files:
                sslabel = 0
                for k,v in specific_symbol.items():
                    if '_pp_' in file:
                        label = file.split('_')[2]
                    else:
                        label = file.split('_')[1]
                        if v in file:
                            sslabel = label.replace(v,k)
                img_name.append(file)
                labels.append(sslabel if sslabel else label)
        print(img_name)
        for img,label in zip(img_name,labels):
            content = '{}\t{}\n'.format(img,label)
            f.write(content)

if __name__ == "__main__":
  txt_path = r'./testlabel.txt'
  img_path = r'./test'
  write_txt(txt_path,img_path)
