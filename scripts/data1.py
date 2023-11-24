import yaml
import os
from PIL import Image
import numpy as np
from easydict import EasyDict
import matplotlib.pyplot as plt 
from tqdm import tqdm 
import xml.etree.ElementTree as ET
import shutil 




def mount_corestorage(local='Z', remote='\\192.168.203.3', username='hehehe', password=123):
    print('access corestorage')
    os.system('net use '+local+': '+remote+' '+password+' /USER:'+username)

def img_resolution_check(img_): # img_ 图像路径
    '''
    核验图像分辨率，保证分辨率大于20000
    '''
    img = Image.open(img_)
    w, h = img.size
    return w*h>=20000

def mkdir_part(file_indx,remote_root,data_root,remotelabel_root=None):
    '''
    创建partxxx文件夹
    '''
    file_indx+=1
    img_path=os.path.join(remote_root,data_root.split('\\')[-1]+'_part'+str(file_indx).zfill(3))
    os.makedirs(img_path, exist_ok=True)
    
    if remotelabel_root!=None:
        label_path=os.path.join(remotelabel_root,data_root.split('\\')[-1]+'_part'+str(file_indx).zfill(3))
        os.makedirs(label_path, exist_ok=True) 
        return file_indx,img_path,label_path
    else:
        return file_indx,img_path


"""

文件原数量:
    miximgs: 1752 张 + 1.db
    calling: 1227 张 + 1.db
    normal: 1978 张 + 1.db
    smoking1: 2168 张 + 1.db
共 7125 张图像

转存数量(resolution>=2万):
    miximgs: 1387 张 √
    calling: 1223 张 √
    normal: 1604 张 √
    smoking1: 2058 张 √
共 6272 张图像

"""

if __name__ == '__main__':

    data_root = 'Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\dianhua\\data1'
    remote_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\images'
   
    os.makedirs(remote_root, exist_ok=True)

    img_ext=['jpg','jpeg','png']

    for root_, dir_, file_ in os.walk(data_root):
        fileindx=0
        indx=0
        if len(dir_)==0:

            img_list=[os.path.join(root_,i) for i in file_ if i.split('.')[-1] in img_ext]
            img_path=os.path.join(remote_root,root_.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
            os.makedirs( img_path, exist_ok=True)

            for x in img_list:
                if img_resolution_check(x):
                    indx+=1
                    shutil.copyfile(x, os.path.join(img_path,x.split('\\')[-1]))
                else: continue
                
                if indx % 1000==0:
                    fileindx,img_path=mkdir_part(fileindx,remote_root,root_)
    

    
   