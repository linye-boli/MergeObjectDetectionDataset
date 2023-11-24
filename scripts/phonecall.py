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

def img_label_check(img_nms, label_nms):
    '''
    核验图像、label文件，保证图像、label文件一一对应
    '''
    img_samples = set(img_nms)
    label_samples = set(label_nms)
    pair_samples = img_samples.intersection(label_samples)
    nolabel_samples = img_samples.difference(label_samples)
    
    return pair_samples,nolabel_samples

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


def class_modi_remote(txt_in,txt_out):
    '''
    txt中的class改为10
    存储
    '''
    
    with open(txt_in,'r+') as file: 
        lines=file.readlines()
        for line in lines:         
            newcotent='10'+' '
            for i in line.split(' ')[1:-1]:newcotent=newcotent+i+' '
            newcotent+=line.split(' ')[-1]
            txt_out.write(newcotent)
                          
    txt_out.close()







if __name__ == '__main__':

    data_root = 'Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\dianhua\\phonecall'
    remote_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\images'
    remotelabel_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\labels'
    os.makedirs(remote_root, exist_ok=True)
    os.makedirs(remotelabel_root, exist_ok=True)

    img_ext=['jpg','jpeg','png']

    img_dict={}
    lab_dict={}
    img_list=[]
    label_list=[]
    fileindx=0
    indx=0
    img_path=os.path.join(remote_root,data_root.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
    os.makedirs(img_path, exist_ok=True)

    for root_, dir_, file_ in os.walk(data_root):
        if len(dir_)==0:
            for i in file_:
                if i.split('.')[-1] in img_ext: 
                    img_dict[i.split('.')[0]]=os.path.join(root_,i) 
                    img_list.append(i.split('.')[0])
                elif i.split('.')[-1] =='txt': 
                    lab_dict[i.split('.')[0]]=os.path.join(root_,i) 
                    label_list.append(i.split('.')[0])
                
    # 图像-标签核验           
    pair_samples,nolabel_samples = img_label_check(img_list,label_list)
            
    #转存图像-标签对
    if len(pair_samples)!=0:
        label_path=os.path.join(remotelabel_root,data_root.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
        os.makedirs(label_path, exist_ok=True)
        
        for nm in tqdm(pair_samples, total=len(pair_samples)):      
            im=img_dict[nm]
            if img_resolution_check(im): # 核验分辨率
                lab=lab_dict[nm]
                indx+=1

                txt_output = open( os.path.join(label_path,nm+'.txt'),'w')
                class_modi_remote(lab,txt_output) 
                shutil.copyfile(im, os.path.join(img_path,nm+'.jpeg'))

            else: continue       
            if indx % 1000==0: #每1000创建一个part文件
                fileindx,img_path,label_path=mkdir_part(fileindx,remote_root,data_root,remotelabel_root)

    #转存无标签图像
    if len(nolabel_samples)!=0:
        for nm in tqdm(nolabel_samples, total=len(nolabel_samples)):
            im=img_dict[nm]
            if img_resolution_check(im): # 核验分辨率
                indx+=1
                shutil.copyfile(im, os.path.join(img_path,nm+'.jpeg'))
            else: continue
            if indx % 1000==0:
                fileindx,img_path=mkdir_part(fileindx,remote_root,data_root)
    
   
    
   