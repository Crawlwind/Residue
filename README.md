# Residue
## Tools:
Python 3.9.10 + Opencv 4.5.5 + Pyqt5

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
![2022 7 1](https://user-images.githubusercontent.com/95983476/176983707-da678902-2ca4-420c-b5f9-cca61b45694c.png)

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
