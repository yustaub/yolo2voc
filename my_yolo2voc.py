# import os
# import cv2
# import pdb
# path='/home/yuwentao/Downloads/zcsj2g2m4c-4/Database1'
# #对每一张图片写xml文件
# def process(file):
#     pass
# #读取指定路径下的txt格式yolo标注并读取对应图片信息
# def read(path):
#     files=os.listdir(path)
#     for file in files:
#         if(file.split('.')[-1]=='txt'):
#             txt_path=os.path.join(path,file)
#             pdb.set_trace()
#             with open(txt_path,'r') as f:
#                 a=f.readlines()
#                 for line in a:
#                     line=line.strip().split(' ')#去掉末尾空格
#                     class_name=int(line[0])
#                     yolo_xc=float(line[1])
#                     yolo_yc=float(line[2])
#                     yolo_w=float(line[3])
#                     yolo_h=float(line[4])
#
#                 print(a)
# read(path)
# Script to convert yolo annotations to voc format
import os
import xml.etree.cElementTree as ET
from PIL import Image
import pdb

ANNOTATIONS_DIR_PREFIX = "/home/yuwentao/Downloads/for_anno"

DESTINATION_DIR = "/home/yuwentao/data/dataset/my_uav/xml_folders2"

CLASS_MAPPING = {
    '0': 'uav'
    # Add your remaining classes here.
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "folder").text = "VOC2007"
    file_name=file_prefix.split('/')[-1]
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_name)

    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(root, "segmented").text = "0"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    #pdb.set_trace()
    file_name=file_prefix.split('/')[-1]
    tree.write("{}/{}.xml".format(DESTINATION_DIR,file_name))


def read_file(file_path):
    #pdb.set_trace()
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.jpg".format(file_prefix)
    img = Image.open(image_file_name)
    #print(img)

    w, h = img.size
    #prueba = "{}/{}".format("Database1", file_path)
    prueba=file_path
    #print(prueba)
    with open(prueba) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            #pdb.set_trace()
            try:
                # PathFileName = "{}/{}".format("Database1", filename)
                # if os.stat(PathFileName).st_size > 0:
                #     print("Si")
                #     read_file(filename)
                new_path=os.path.join(ANNOTATIONS_DIR_PREFIX,filename)
                read_file(new_path)
            except:
                print("No")

        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()