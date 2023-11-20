import yaml
import os
from PIL import Image
import numpy as np
from easydict import EasyDict
import matplotlib.pyplot as plt 
from tqdm import tqdm 
import shutil 

def img_mask_check(img_nms, mask_nms):
    '''
    核验图像、mask文件，保证图像、mask文件一一对应，返回一一对应的图像列表、mask文件列表
    
    img_nms : 图像文件名称列表
    mask_nms : mask文件名称列表

    '''
    img_samples = set([nm.split('.')[0] for nm in img_nms])
    mask_samples = set([nm.split('.')[0].split('_')[0] for nm in mask_nms])
    samples = img_samples.intersection(mask_samples)
    pairs = [(s+'.png', s+'_mask.png') for s in sorted(list(samples))]

    return pairs

def mask2bbox(mask):
    H, W = mask.shape
    pids = np.unique(mask)

    bboxes = []
    for i in pids:
        if i != 0 :
            indices = np.argwhere(mask == i)
            ymax, ymin = indices[:,0].max(), indices[:,0].min()
            xmax, xmin = indices[:,1].max(), indices[:,1].min()
            
            xc = (xmax + xmin)/2
            yc = (ymax + ymin)/2
            width = xmax - xmin
            height = ymax - ymin 

            bboxes.append([4, xc/W, yc/H, width/W, height/H]) # 4 表示"人物-全身", 参考obj_code.yaml
    
            # 合理性检验
            # plt.imshow(img)
            # plt.scatter(xc, yc)
            # plt.scatter([xc-width/2, xc+width/2], [yc, yc])
            # plt.scatter([xc, xc], [yc-height/2, yc+height/2])
            # plt.show()

    return bboxes

def save_bboxes(bboxes, outpath):
    with open(outpath, 'w') as f:
        for bbox in bboxes:
            f.write(' '.join([str(x) for x in bbox]))
            f.write('\n')

if __name__ == '__main__':

    data_root = 'C:\\Users\\LINYE\Desktop\\工作内容\\merge_data\\PennFudanPed\\PennFudanPed'
    obj_code_path = 'C:\\Users\\LINYE\Desktop\\工作内容\\merge_data\\MergeObjectDetectionDataset\\obj_code.yaml'

    remoteimg_root = 'Z:\\images\\PennFudanPed'
    remotelabel_root = 'Z:\\labels\\PennFudanPed'

    os.makedirs(remoteimg_root, exist_ok=True)
    os.makedirs(remotelabel_root, exist_ok=True)

    locallabel_root = 'C:\\Users\\LINYE\Desktop\\工作内容\\merge_data\\MergeObjectDetectionDataset'

    # 图像目录读取
    img_root = os.path.join(data_root, 'PNGImages') # 图像根目录    
    img_nms = os.listdir(img_root) # 图像文件名称列表

    # 标签目录读取
    mask_root = os.path.join(data_root, 'PedMasks')
    mask_nms = set(os.listdir(mask_root)) # 图像文件名称列表

    # 图像-标签核验
    pairs = img_mask_check(img_nms, mask_nms)
    npairs = len(pairs)

    # 目标检测词典
    with open(obj_code_path, encoding='utf-8') as f:
        obj_code_dict = EasyDict(yaml.full_load(f))

    # 目标筛选条件
    ## 选择4: 人物-全身

    # 图像-标签处理
    remoteimg_paths = []
    remotelabel_paths = []
    for img_nm, mask_nm in tqdm(pairs, total=npairs):
        img_path = os.path.join(img_root, img_nm)
        mask_path = os.path.join(mask_root, mask_nm)

        # 图像转存
        imgs_remotepath = os.path.join(remoteimg_root, img_nm)
        shutil.copyfile(img_path, imgs_remotepath)
        
        # 载入mask
        mask = np.array(Image.open(mask_path))
        bboxes = mask2bbox(mask)

        # 存储bbox
        bboxes_outnm = img_nm.replace('png', 'txt')
        bboxes_outpath = os.path.join(remotelabel_root, bboxes_outnm)
        save_bboxes(bboxes, bboxes_outpath)

        remoteimg_paths.append(imgs_remotepath)
        remotelabel_paths.append(bboxes_outpath)
