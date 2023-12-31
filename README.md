# MergeObjectDetectionDataset
Merged Object Detection Dataset

## 项目目标

构建用于目标检测(矩形框检测)的可持续添加数据集，目标类别如下：
* 人物
    1. 人脸
    2. 人头
    3. 上半身
    4. 下半身
    5. 全身
* 烟
    1. 烟在手
    2. 烟在嘴
    3. 烟(包括单支烟、多支烟、烟屁、烟盒、烟斗、烟嘴等等)
* 手机
    1. 手机在手
    2. 手机在头
    3. 手机(智能手机，不包括固定电话)
* 头盔
    1. 安全帽
    2. 帽子
    3. 其他头盔
* 动作
    1. 下蹲
    2. 摔倒
    3. 跑
    4. 跳
    5. 打架
    6. 躺下
    7. 攀爬
* 载具
    1. 家用车
    2. 货车
    3. 快递车
    4. 工程车
    5. 警车
    6. 救护车
* 身份
    1. 快递员
    2. 外卖员
    3. 保安
    4. 医护
    5. 警察
* 消防
    1. 灭火器
    2. 防火栓
    3. 安全门
* 设施状态
    1. 安全门开


## 监控视角数据集下载

1. https://tianchi.aliyun.com/dataset/146450
2. https://blog.csdn.net/Strive_For_Future/article/details/114854674
3. https://viratdata.org/#getting-data

## 数据集存储

### 目标存储位置

\\192.168.203.3\BoLiTech\RDTeam\01_BDAI\merged_data

### merge_data 的文件结构为

- merged_data
    - images
        - xxx_part001
        - xxx_part002
        - xxx_part003
        - yyy_part001
        - yyy_part002
        - ...
    - labels
        - xxx
        - yyy 
        - ...
    - Annotations
        - xxx_part001
            - cls1_anns（yolo 格式数据输出）
            - cls2_anns
            - cls3_anns
            - ...
        - xxx_part002
            - cls1_anns
            - cls2_anns
            - cls3_anns
            - ...
        - ...
        
            

## 原始数据集处理脚本

## 原始数据集MetaInfo

## 目标检测数据格式
- 数据对格式：
    - 图像名称：img_nm.jpg/img_nm.png
    - 标签名称：img_nm.txt

- 标签内容：

## windows 本地链接NAS服务器
- NAS服务器地址：\\192.168.203.3
- 用户名：linye
- 密码：123
