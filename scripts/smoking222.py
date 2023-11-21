import yaml
import os
from PIL import Image
import numpy as np
from easydict import EasyDict
import matplotlib.pyplot as plt 
from tqdm import tqdm 
import xml.etree.ElementTree as ET
import shutil 
import re
def mount_corestorage(local='Z', remote='\\192.168.203.3', username='hehehe', password=123):
    print('access corestorage')
    os.system('net use '+local+': '+remote+' '+password+' /USER:'+username)

def xml2txt(xmlpath,savepath,savename):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    output = open(os.path.join(savepath, savename),'w')

    for obj in root.findall('object'):
        
        label = obj.find('name').text
        w= int(root.find('size/width').text)
        h = int(root.find('size/height').text)
        xmin = int(obj.find('bndbox/xmin').text)/w
        ymin = int(obj.find('bndbox/ymin').text)/h
        xmax = int(obj.find('bndbox/xmax').text)/w
        ymax = int(obj.find('bndbox/ymax').text)/h

        cent_x=(xmax+xmin)/2
        cent_y=(ymax+ymin)/2
        weight=xmax-xmin
        height=ymax-ymin
        
        if label == 'smoking':
            object_class=7
        output.write('%s\t%.6f\t%.6f\t%.6f\t%.6f\n' % (object_class,cent_x,cent_y,weight,height))
    output.close()


if __name__ == '__main__':

    data_root = 'Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\xiyan\\smoking222'
    remote_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\images'
    remotelabel_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\labels'
    os.makedirs(remote_root, exist_ok=True)
    os.makedirs(remotelabel_root, exist_ok=True)

    #dataroot=[os.path.join(data_root,x) for x in os.listdir(data_root) if os.path.isdir(os.path.join(data_root,x))]
    #dataroot=[os.path.join(data_root,x) for x in os.listdir(data_root) if x=='smoking' or x=='smoking2']
    dataroot=[os.path.join(data_root,x) for x in os.listdir(data_root) if  x=='smoking2']
    print(dataroot)

 

    for i in dataroot:
        

        img_list=[]
        label_list=[]
        nolabel_list=[]
        fileindx=0
        indx=0

        img_path=os.path.join(remote_root,i.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
        os.makedirs(img_path, exist_ok=True)

        for root_, dir_, file_ in os.walk(i):
            if len(dir_)==0:
 
                img_samples = set([x.split('.')[0] for x in file_ if x.split('.')[-1]=='jpg'])
                label_samples = set([x.split('.')[0] for x in file_ if x.split('.')[-1]=='xml'])
                
                pair_samples = img_samples.intersection(label_samples) #图像label对
                nolabel_samples=img_samples.difference(pair_samples) #无label图像
                
                for pair in sorted(list(pair_samples)):
                    img_list.append(os.path.join(root_,pair+'.jpg'))
                    label_list.append(os.path.join(root_,pair+'.xml'))
                for nolabel in sorted(list(nolabel_samples)):
                    nolabel_list.append(os.path.join(root_,nolabel+'.jpg'))
                
            
        # 存图像标签对
        if len(img_list)==len(label_list) and len(label_list)!=0: 
            label_path=os.path.join(remotelabel_root,i.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
            os.makedirs(label_path, exist_ok=True)

            for x in range(len(label_list)):
                indx+=1
               
                #统一命名，转存
                new_img=img_list[x].split('\\')[-2]+'_'+img_list[x].split('\\')[-1].split('-')[-1] 
                new_label=label_list[x].split('\\')[-2]+'_'+label_list[x].split('\\')[-1].split('-')[-1].split('.')[0]+'.txt'
       
                shutil.copyfile(img_list[x], os.path.join(img_path,new_img))
                xml2txt(label_list[x],label_path,new_label)

                if indx % 1000==0:
                    fileindx+=1
                    img_path=os.path.join(remote_root,i.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
                    label_path=os.path.join(remotelabel_root,i.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
                    os.makedirs(img_path, exist_ok=True)
                    os.makedirs(label_path, exist_ok=True)


        # 存无标签图像
        for y in range(len(nolabel_list)):
            indx+=1

            #统一命名，转存
            new_nolabel=nolabel_list[y].split('\\')[-2]+'_'+nolabel_list[y].split('\\')[-1].split('-')[-1] 
            shutil.copyfile(nolabel_list[y], os.path.join(img_path,new_nolabel))

            if indx % 1000==0:
                fileindx+=1
                img_path=os.path.join(remote_root,i.split('\\')[-1]+'_part'+str(fileindx).zfill(3))
                os.makedirs(img_path, exist_ok=True)

