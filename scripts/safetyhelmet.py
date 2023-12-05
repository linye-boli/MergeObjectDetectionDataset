import yaml
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm 
import shutil 
import openpyxl
import xml.etree.ElementTree as ET


def mount_corestorage(local='Z', remote='\\192.168.203.3', username='hehehe', password=123):
    print('access corestorage')
    os.system('net use '+local+': '+remote+' '+password+' /USER:'+username)


def img_label_check(img_nms, label_nms):
    '''
    核验图像、label文件，保证图像、label文件一一对应
    '''
    img_samples = set([nm.split('.')[0] for nm in img_nms])
    label_samples = set([lb.split('.')[0] for lb in label_nms])
    pair_samples = img_samples.intersection(label_samples)
    nolabel_samples = img_samples.difference(label_samples)
    return pair_samples,nolabel_samples


def img_resolution_check(img_): # img_ 图像路径
    '''
    核验图像分辨率，保证分辨率大于10万
    '''
    img = Image.open(img_)
    w, h = img.size
    return w*h>=100000


def mkdir_part(file_indx,file_name,remote_root,data_root,remotelabel_root=None):
    '''
    创建partxxx文件夹
    '''
    file_indx+=1
    img_path=os.path.join(remote_root,file_name+str(file_indx).zfill(3))
    os.makedirs(img_path, exist_ok=True)
    if remotelabel_root!=None:
        label_path=os.path.join(remotelabel_root,file_name+str(file_indx).zfill(3))
        os.makedirs(label_path, exist_ok=True) 
        return file_indx,img_path,label_path
    else:
        return file_indx,img_path
    

def xml2txt(xmlpath,savepath,savename):
    '''
     xml转txt
    '''
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
        # 只有 hat(安全帽 11)，person(人头 1) 两种label
        if label == 'hat':  
            object_class=11  
        else: 
            object_class=1                        
        output.write('%s %.6f %.6f %.6f %.6f\n' % (object_class,cent_x,cent_y,weight,height))
    output.close()


    """

原数量:
    JPEGImages: 7581 (.jpg/.JPG)
    Annotations: 7581 (.xml)

转存数量(resolution>=10万):
    图像: 7268 (.jpg) √
    标签: 7268 (.txt) √

"""

if __name__ == '__main__':

    data_root = 'Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\safetyhelmet\\JPEGImages'
    label_root='Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\safetyhelmet\\Annotations'
    remote_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\images'
    remotelabel_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\labels'

    file_name='safetyhelmet_part' # 文件名
    img_dict={}
    lab_dict={}
    fileindx=0
    indx=0
    list_=[]
    
    img_path=os.path.join(remote_root,file_name+str(fileindx).zfill(3))
    os.makedirs(img_path, exist_ok=True)

    # 图像标签目录读取
    mg_nms = os.listdir(data_root)
    lab_nms=os.listdir(label_root)

    for i in mg_nms:
        img_dict[i.split('.')[0]]=os.path.join(data_root,i)
    for j in lab_nms:
        lab_dict[j.split('.')[0]]=os.path.join(label_root,j) 

    # 图像-标签核验
    pair_samples,nolabel_samples=img_label_check(mg_nms,lab_nms)

    # 转存图像-标签对
    if len(pair_samples)!=0:
        label_path=os.path.join(remotelabel_root,file_name+str(fileindx).zfill(3))
        os.makedirs(label_path, exist_ok=True)
        
        for nm in tqdm(pair_samples, total=len(pair_samples)):      
            im=img_dict[nm]
            if img_resolution_check(im): # 核验分辨率
                lab=lab_dict[nm]
                indx+=1
                #图像转存
                shutil.copyfile(im, os.path.join(img_path,nm+'.jpg'))
                #标签xml2txt，转存
                new_label=nm+'.txt'
                xml2txt(lab,label_path,new_label)
            else: continue      
            if indx % 1000==0: #每1000创建一个part文件
                fileindx,img_path,label_path=mkdir_part(fileindx,file_name,remote_root,data_root,remotelabel_root)   
  
    # 转存无标签图像
    if len(nolabel_samples)!=0:
        for nm in tqdm(nolabel_samples, total=len(nolabel_samples)):
            im=img_dict[nm]
            if img_resolution_check(im): # 核验分辨率
                indx+=1
                shutil.copyfile(im, os.path.join(img_path,nm+'.jpg'))
            else: continue
            if indx % 1000==0:
                fileindx,img_path=mkdir_part(fileindx,file_name,remote_root,data_root)


