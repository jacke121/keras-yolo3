import numpy as np
import os
import xml.etree.ElementTree as ET


classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes = ["mouse"]
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
def parse_voc_annotation(ann_dir, img_dir, labels=[]):
    all_imgs = []
    seen_labels = {}
    
    for ann in sorted(os.listdir(ann_dir)):
        img = {'object':[]}

        tree = ET.parse(ann_dir + ann)
        # tree = ET.parse(in_file)
        root = tree.getroot()

        img['filename'] = img_dir + root.find('filename').text
        size = root.find('size')

        img['width'] = int(size.find('width').text)
        img['height'] =  int(size.find('height').text)
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for objnode in root.iter('object'):
            objs = {}
            difficult = objnode.find('difficult').text
            cls = objnode.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            objs['name'] = cls
            if objs['name'] in seen_labels:
                seen_labels[objs['name']] += 1
            else:
                seen_labels[objs['name']] = 1

            img['object'] += [objs]
            xmlbox = objnode.find('bndbox')

            objs['xmin'] = int(round(float(xmlbox.find('xmin').text)))
            objs['ymin'] = int(round(float(xmlbox.find('ymin').text)))
            objs['xmax'] = int(round(float(xmlbox.find('xmax').text)))
            objs['ymax'] = int(round(float(xmlbox.find('ymax').text)))

        if len(img['object']) > 0:
            all_imgs += [img]
        # for elem in tree.iter():
        #     # if 'filename' in elem.tag:
        #     #     img['filename'] = img_dir + elem.text
        #     # if 'width' in elem.tag:
        #     #     img['width'] = int(elem.text)
        #     # if 'height' in elem.tag:
        #     #     img['height'] = int(elem.text)
        #     if 'object' in elem.tag or 'part' in elem.tag:
        #         obj = {}
        #
        #         for attr in list(elem):
        #             if 'name' in attr.tag:
        #                 obj['name'] = attr.text
        #
        #                 if obj['name'] in seen_labels:
        #                     seen_labels[obj['name']] += 1
        #                 else:
        #                     seen_labels[obj['name']] = 1
        #
        #                 if len(labels) > 0 and obj['name'] not in labels:
        #                     break
        #                 else:
        #                     img['object'] += [obj]
        #
        #             if 'bndbox' in attr.tag:
        #                 for dim in list(attr):
        #                     if 'xmin' in dim.tag:
        #                         obj['xmin'] = int(round(float(dim.text)))
        #                     if 'ymin' in dim.tag:
        #                         obj['ymin'] = int(round(float(dim.text)))
        #                     if 'xmax' in dim.tag:
        #                         obj['xmax'] = int(round(float(dim.text)))
        #                     if 'ymax' in dim.tag:
        #                         obj['ymax'] = int(round(float(dim.text)))
        #
        # if len(img['object']) > 0:
        #     all_imgs += [img]
                        
    return all_imgs, seen_labels