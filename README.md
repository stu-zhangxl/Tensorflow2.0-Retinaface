# Tensorflow2.0-Retinaface
Retinaface net implement by tensorflow2.0


这里根据前辈的项目进行实现并进行自己的相关方向进行编写相关代码. 

这里是没有限制喂进模型的图片的shape, 如果想改的话, 可以修改如下文件: 
/nets/retinaface.py
中函数 `RetinaFace` 中 `inputs` 部分: 
```python
inputs = Input(shape=(None, None, 3))
# inputs = Input(shape=(224, 224, 3))
# inputs = Input(shape=(1330, 1330, 3))
```
可以改成注释中的形式. 
如果改的较小, 输入的图片很大, 整体效果就很差. 

