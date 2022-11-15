from retinaface import Retinaface
from utils.config import cfg_mnet, cfg_re50
import os
import cv2

if __name__ == '__main__':
    model = Retinaface()

    # model_path = "model_data/retinaface_mobilenet025.h5"
    #------------------------------------------------------#
    #   载入预训练权重
    #------------------------------------------------------#
    # print('Load weights {}.'.format(model_path))
    # model.load_weights(model_path, by_name=True, skip_mismatch=True)
    img = 'img/timg.jpg'
    image = cv2.imread(img) 
    # 如果在网络中限制了输入图片的shape, 那么图片就需要进行如下resize处理
    # image = cv2.resize(image,(224, 224))
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    r_image = model.detect_image(image)
    r_image = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
    cv2.imshow("after",r_image)
    cv2.waitKey(0)
