# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join

classes = ["table"]  # 自己数据集有哪些类别写哪些类，按照顺序


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(r'E:\YOLO-v5-master\datasets\score\labels\val/%s.xml' % (image_id), encoding='utf-8')
    out_file = open('labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


val_percent = 0.1  # 测试集占总数据集的比例，默认0.1，如果测试集和训练集已经划分开了，则修改相应代码
data_path = r'E:/YOLO-v5-master/datasets/score/images/'  # 在darknet文件夹的相对路径，见github的说明，根据自己需要修改，注意此处也可以用绝对路径
if not os.path.exists('labels/'):
    os.makedirs('labels/')
image_ids = [f for f in os.listdir(r'E:\YOLO-v5-master\datasets\score\labels\val')]  # 存放XML数据的文件夹
train_file = open('train.txt', 'w')
val_file = open('val.txt', 'w')
for i, image_id in enumerate(image_ids):
    if image_id[-3:] == "xml":  # 有些时候jpg和xml文件是放在同一文件夹下的，所以要判断一下后缀
        if i < (len(image_ids) * val_percent):
            val_file.write(data_path + '%s\n' % (image_id[:-3] + 'jpg'))
        else:
            train_file.write(data_path + '%s\n' % (image_id[:-3] + 'jpg'))
    convert_annotation(image_id[:-4])
train_file.close()
val_file.close()
