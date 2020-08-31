# Intelligent-Traffic-Scene 
# 交通场景智能应用软件


## 1️⃣ 功能列表
✅ 利用YOLOv3实现车辆、行人、红绿灯检测  
✅ 利用HSV原理检测红绿灯颜色  
✅ 利用HyperLPR实现车牌检测  
✅ 目标分类统计、路段车流量统计，并将结果存储在Excel文件中  
⭕ 更多高级的行为识别功能等待开发......  


## 2️⃣ 源码说明
通过Anaconda建立虚拟环境，cd至项目目录下，利用`requirements.txt`文件安装所需环境。  

    pip install -r requirements.txt
运行`Video_Player.py`文件，显示软件主界面。

    python Video_Player.py


### `Video_Player.py`
Pyqt5的软件界面。
### `Traffic_Scene_Detection.py`
程序主要文件，进行读取视频，目标检测识别。
### `utils.py`
保存各种对当前帧进行的操作。


## 3️⃣ 软件使用说明
![dOKwh8.png](https://s1.ax1x.com/2020/08/31/dOKwh8.png)

运行程序后，主界面如上图所示，中间界面为视频播放区域，下方依次为：  
① 工具图标：选择视频文件进行识别检测处理；   
② 文件夹图标：选择视频文件进行播放；  
③ 箭头图标及进度条：播放/暂停键，右侧为视频播放进度条。  

界面最下方为当前状态提示信息，默认情况下显示信息如图所示。使用处理按钮选中文件以后，程序进入处理状态，此时提示信息会变为`视频处理中，请耐心等待。`。视频处理完毕，结果视频将自动保存，提示信息为`结果已存放于: +"存放路径"`。



## 4️⃣ 软件截图
[![dOGFEj.png](https://s1.ax1x.com/2020/08/31/dOGFEj.png)](https://imgchr.com/i/dOGFEj)


## 5️⃣ 编写过程中使用的开源代码/教程
🚩 [HyperLPR高性能车牌检测](https://github.com/zeusees/HyperLPR)  
🚩 [YOLOv3安装教程](https://www.bilibili.com/video/BV1r5411t7Db)  
🚩 [OpenCV教程](https://www.bilibili.com/video/BV1oJ411D71z)




