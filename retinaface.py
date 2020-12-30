import os
import cv2
import tensorflow.keras
import pickle
import colorsys
import numpy as np
import tensorflow as tf
from nets.retinaface import RetinaFace
from PIL import Image,ImageFont, ImageDraw
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from utils.anchors import Anchors
from utils.config import cfg_mnet,cfg_re50
from utils.utils import BBoxUtility,letterbox_image,retinaface_correct_boxes
import time
class Retinaface(object):
    _defaults = {
        "model_path": 'model_data/retinaface_mobilenet025.h5',
        "backbone": "mobilenet",
        "confidence": 0.5,
        
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#
    #   初始化Retinaface
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        if self.backbone == "mobilenet":
            self.cfg = cfg_mnet
        else:
            self.cfg = cfg_re50
        self.bbox_util = BBoxUtility()
        self.generate()

    #---------------------------------------------------#
    #   获得所有的分类
    #---------------------------------------------------#
    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'tensorflow.keras model or weights must be a .h5 file.'

        # 加快模型训练的效率
        print('Loading weights into state dict...')
        # 载入模型
        self.retinaface = RetinaFace(self.cfg, self.backbone)
        self.retinaface.load_weights(self.model_path)
        print('{} model, anchors loaded.'.format(self.model_path))

    @tf.function
    def get_pred(self, photo):
        preds = self.retinaface(photo, training=False)
        return preds

    #---------------------------------------------------#
    #   检测图片
    #---------------------------------------------------#
    def detect_image(self, image):
        old_image = image.copy()

        image = np.array(image,np.float32)
        im_height, im_width, _ = np.shape(image)

        scale = [im_width, im_height, im_width, im_height]
        scale_for_landmarks = [im_width, im_height, im_width, im_height,
                               im_width, im_height, im_width, im_height,
                               im_width, im_height]

        # 图片预处理，归一化
        photo = np.expand_dims(preprocess_input(image),0)
        anchors = Anchors(self.cfg, image_size=(im_height, im_width)).get_anchors()

        preds = self.get_pred(photo)
        preds = [pred.numpy() for pred in preds]

        # 将预测结果进行解码和非极大抑制
        results = self.bbox_util.detection_out(preds,anchors,confidence_threshold=self.confidence)

        if len(results)<=0:
            return old_image
        results = np.array(results)
        results[:,:4] = results[:,:4]*scale
        results[:,5:] = results[:,5:]*scale_for_landmarks

        for b in results:
            text = "{:.4f}".format(b[4])
            b = list(map(int, b))
            cv2.rectangle(old_image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
            cx = b[0]
            cy = b[1] + 12
            cv2.putText(old_image, text, (cx, cy),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

            # landms
            cv2.circle(old_image, (b[5], b[6]), 1, (0, 0, 255), 4)
            cv2.circle(old_image, (b[7], b[8]), 1, (0, 255, 255), 4)
            cv2.circle(old_image, (b[9], b[10]), 1, (255, 0, 255), 4)
            cv2.circle(old_image, (b[11], b[12]), 1, (0, 255, 0), 4)
            cv2.circle(old_image, (b[13], b[14]), 1, (255, 0, 0), 4)

        return old_image

