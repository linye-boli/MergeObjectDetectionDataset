import yaml
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm 
import shutil 

def mount_corestorage(local='Z', remote='\\192.168.203.3', username='hehehe', password=123):
    print('access corestorage')
    os.system('net use '+local+': '+remote+' '+password+' /USER:'+username)


    

if __name__ == '__main__':

    data_root = 'Z:\\RDTeam\\01_BDAI\\OD_dataset_20231110\\xiyan\\smokingVSnotsmoking\\dataset'
    remoteimg_root = 'Z:\\RDTeam\\01_BDAI\\merged_data\\images'
    
    os.makedirs(remoteimg_root, exist_ok=True)
    img_list=[]

    for root_, dir_, file_ in os.walk(data_root):
        if len(dir_)==0:
            for img in file_: 
                img_list.append(os.path.join(root_,img))
  
    indx=0
    fileindx=0
    
    os.makedirs(os.path.join(remoteimg_root,'smokingVSnotsmoking_part'+str(fileindx).zfill(3)), exist_ok=True)

    for img_nmpath in tqdm(img_list, total=len(img_list)):
        img_nm=img_nmpath.split('\\')[-1]

        if img_nm.endswith('.jpg') or img_nm.endswith('.jpeg') or img_nm.endswith('.JPG'):
            indx+=1  
            # jepg、JPG转为jpg  
            newname='.'+img_nm.split('.')[-1]
            newimg_nm=img_nm.replace(newname, ".jpg")
            remotfile_path=os.path.join(remoteimg_root,'smokingVSnotsmoking_part'+str(fileindx).zfill(3),newimg_nm)
            shutil.copyfile(img_nmpath, remotfile_path) # 转存

        if indx % 1000==0:
            fileindx+=1
            os.makedirs(os.path.join(remoteimg_root,'smokingVSnotsmoking_part'+str(fileindx).zfill(3)), exist_ok=True)
    