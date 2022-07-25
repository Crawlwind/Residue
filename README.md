# Residue
## Tools:
Python 3.9.10 + Opencv 4.5.5 + Pyqt5

## Usage:
Run main.py
```
cd src
python main.py
```

## Log:
**2022.6.15:**

完成：SLIC

**2022.6.29:**

完成：
- 界面搭建
- 打开文件

缺乏：
- slic.py的迁移
- 进度条显示相应数值
- 图片显示 exitexited with code=3221226505
- 保存图片

**2022.7.1:**

完成：
- silc.py的迁移
- 进度条显示相应数值
- 图片显示
- 保存图片

缺乏：
- Proceed之后拖拽进度条会直接处理已proceed的图片
<img src="https://user-images.githubusercontent.com/95983476/180357254-54057dec-ea26-425b-adc9-0bd552c73022.png" width="500">

**2022.7.2:**

完成：拖动进度条实现实时更新

**2022.7.18:**

完成：
- 确认centers，paint them
- 确认clusters，paint them

**2022.7.19:**

完成：
- superpixel分割和label分成两个界面
- label page的初步搭建
- get mouse position
- 当前鼠标位置和原始图片坐标系转换
- 确认当前鼠标位置像素点所属cluster
- save image

**2022.7.20:**
- quick label:根据像素点R值，确认当前cluster的label
- editable text:可编辑quick label生成的label
- generate cover/clear cover
- apply:确认检查单词拼写情况Error

**2022.7.21:**
完成：所有基础功能，但美观与更便捷的设置及更有效的功能仍待改进
<img src= "https://user-images.githubusercontent.com/95983476/180356985-775a8c21-9dda-4b41-9bb9-05f07d91ddb0.png" width="500">

**2022.7.25:**

完成：apply和save的comboBox及其对应的function，从我的角度而言，工具已经完成

<img src= "https://user-images.githubusercontent.com/95983476/180786535-4b014c21-e39b-4c07-b26a-be6e1aec5e51.png" width="500">

