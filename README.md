# cover-crt-rapid-editor
 rapid src img editor for css `object-positon`
# 运行库
程序调用python内置的`os`及`tkinter`库

需额外安装Pillow库

`pip install Pillow`
# 使用方法
## 1. 将全部待处理图片放入pics文件夹
（或修改代码`line 11`到其他路径）

`image_dir = "./pics"`

## 2. 运行`cover-crt.py`
* 在输入框中输入期望的选取框高度（默认500px）

* 拖动选取框至想要的位置（程序中的`cover_crt=`会在释放鼠标时更新）
* 点击`重命名并下一张`（文件将会以“原文件名”+“cover_crt-`xxxxx`”格式被重命名）
* 程序并不会记录工作进度，请及时将处理完的图片移出工作目录