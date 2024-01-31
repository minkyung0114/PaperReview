import os
import cv2
import xml.etree.ElementTree as ET
import glob
from shutil import copyfile
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageEnhance, ImageChops, ImageFilter
import math
print(sys.getdefaultencoding())
print(f"원하는 것을 선택하세요 ")
print(f"1.HorizontalShift   2.VerticalShift   3.HorizontalFlip   4.VerticalFlip   5.Rotation")
choice_option = str(input())
print(f"이미지 경로입력하세요(마지막 \를 제외)!")

img_path = str(input())
xml_path = glob.glob(img_path)
img_files = glob.glob(img_path + '/*.jpg' or '/*.bmp' or '/*.BMP' or '/*.JPG')
xml_files = glob.glob(img_path + '/*.xml' or '/*.XML')

folder_name_hs = str("aug_H_Shift")
folder_name_vs = str("aug_V_Shift")
folder_name_hf = str("aug_H_Flip")
folder_name_vf = str("aug_V_Flip")
folder_name_rt = str("aug_Rotation")
num_shift = [*range(1, 31, 5)]
new_corners = []
corners = []
new_rot_corners = []
num_rot = [*range(30, 360, 60)]
# width, height, _ = image.shape
# center_img = (width // 2, height // 2)


##################### Horozontal Shift ##################
def imgHshift(img_files):
    print(f"|**************** aug_shift폴더에 저장됩니다.****************|")
    for i in num_shift:
        #print(f"i:{i}")
        for j in range(len(img_files)):
            #print(f"files[j]:{img_files}")
            replace_path = img_files[j].replace("\\", "/")
            image = cv2.imread(replace_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            width, height,_ = image.shape
            base_name = os.path.basename(replace_path).split('.')[0]
            M = np.float32([[1, 0, i], [0, 1, 0]])
            shifted = cv2.warpAffine(image, M, (height, width))
            os.makedirs(os.path.join(img_path, folder_name_hs), exist_ok=True)
            cv2.imwrite(os.path.join(img_path,folder_name_hs,f"{base_name}_HS{i}.jpg"),shifted)

def Hshift_bbox_coordinates(num_shift, xmin, xmax):
    return xmin + num_shift, xmax + num_shift

def xmlHshift(xml_file, i):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for fln in root.iter('filename'):
        original_filename = fln.text
        new_name = f"_HS{i}.jpg"
        modified_filename = original_filename.replace('.jpg', new_name)
        fln.text = modified_filename
        #tree.write(modified_filename)
    for path in root.iter('path'):
        original_path = path.text
        new_name = f"_HS{i}.jpg"
        modified_path = original_path.replace('.jpg', new_name)
        path.text = modified_path
        #tree.write(modified_path)
    for obj in root.iter('object'):
        for bbox in obj.iter('bndbox'):
            xmin = int(bbox.find('xmin').text)
            xmax = int(bbox.find('xmax').text)
            new_xmin, new_xmax = Hshift_bbox_coordinates(i, xmin, xmax)
            bbox.find('xmin').text = str(new_xmin)
            bbox.find('xmax').text = str(new_xmax)

    base_name, extension = os.path.splitext(os.path.basename(xml_file))
    new_xml_name = f"{base_name}_HS{i}.xml"
    output_xml_path = os.path.join(img_path, folder_name_hs, new_xml_name)
    tree.write(output_xml_path)

def xmlHshift_all(xml_files, num_shift):
    for xml_file in xml_files:
        for i in num_shift:
            xmlHshift(xml_file, i)

##################### Vertical Shift ##################
def imgVshift(img_files):
    print(f"|**************** aug_shift폴더에 저장됩니다.****************|")
    for i in num_shift:
        #print(f"i:{i}")
        for j in range(len(img_files)):
            #print(f"files[j]:{img_files}")
            replace_path = img_files[j].replace("\\", "/")
            image = cv2.imread(replace_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            width, height,_ = image.shape
            base_name = os.path.basename(replace_path).split('.')[0]
            M = np.float32([[1, 0, 0], [0, 1, i]])
            shifted = cv2.warpAffine(image, M, (height, width))
            os.makedirs(os.path.join(img_path, folder_name_vs), exist_ok=True)
            cv2.imwrite(os.path.join(img_path,folder_name_vs,f"{base_name}_VS{i}.jpg"),shifted)

def Vshift_bbox_coordinates(num_shift, ymin, ymax):
    return ymin + num_shift, ymax + num_shift

def xmlVshift(xml_file, i):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for fln in root.iter('filename'):
        original_filename = fln.text
        new_name = f"_VS{i}.jpg"
        modified_filename = original_filename.replace('.jpg', new_name)
        fln.text = modified_filename
        #tree.write(modified_filename)
    for path in root.iter('path'):
        original_path = path.text
        new_name = f"_VS{i}.jpg"
        modified_path = original_path.replace('.jpg', new_name)
        path.text = modified_path
        #tree.write(modified_path)
    for obj in root.iter('object'):
        for bbox in obj.iter('bndbox'):
            ymin = int(bbox.find('ymin').text)
            ymax = int(bbox.find('ymax').text)
            new_ymin, new_ymax = Vshift_bbox_coordinates(i, ymin, ymax)
            bbox.find('ymin').text = str(new_ymin)
            bbox.find('ymax').text = str(new_ymax)

    base_name, extension = os.path.splitext(os.path.basename(xml_file))
    new_xml_name = f"{base_name}_VS{i}.xml"
    output_xml_path = os.path.join(img_path, folder_name_vs, new_xml_name)
    tree.write(output_xml_path)

def xmlVshift_all(xml_files, num_shift):
    for xml_file in xml_files:
        for i in num_shift:
            xmlVshift(xml_file, i)

##################### Horizontal Flip ##################
def imgHflip(img_files):
    print(f"|**************** aug_h_flip 폴더에 저장됩니다.****************|")
    for idx, file in enumerate(img_files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        flip_image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        os.makedirs(os.path.join(img_path, folder_name_hf), exist_ok=True)
        flip_image.save(os.path.join(img_path, folder_name_hf, f"{base_name}_HF.jpg"))

def HFlip_bbox_coordinates(image_width, xmin, xmax):
    return image_width - xmin, image_width - xmax

def xmlHflip(xml_file):
    print(f"xml_file:{xml_file}")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    image_width = int(root.find('size/width').text)
    for fln in root.iter('filename'):
        original_filename = fln.text
        new_name = f"_HF.jpg"
        modified_filename = original_filename.replace('.jpg', new_name)
        fln.text = modified_filename
        #tree.write(modified_filename)
    for path in root.iter('path'):
        original_path = path.text
        new_name = f"_HF.jpg"
        modified_path = original_path.replace('.jpg', new_name)
        path.text = modified_path
        #tree.write(modified_path)
    for obj in root.iter('object'):
        for bbox in obj.iter('bndbox'):
            xmin = int(bbox.find('xmin').text)
            xmax = int(bbox.find('xmax').text)
            new_xmin, new_xmax = HFlip_bbox_coordinates(image_width, xmin, xmax)
            bbox.find('xmin').text = str(new_xmin)
            bbox.find('xmax').text = str(new_xmax)

    base_name, extension = os.path.splitext(os.path.basename(xml_file))
    new_xml_name = f"{base_name}_HF.xml"
    new_path = os.path.join(img_path, folder_name_hf, new_xml_name)
    print(f"new_path:{new_path}")
    output_xml_path = os.path.join(img_path, folder_name_hf, new_xml_name)
    tree.write(output_xml_path)

def xmlHflip_all(xml_files):
    for xml_file in xml_files:
        xmlHflip(xml_file)


##################### Vertical Flip ##################
def imgVflip(img_files):
    print(f"|**************** aug_v_flip 폴더에 저장됩니다.****************|")
    for idx, file in enumerate(img_files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        flip_image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        os.makedirs(os.path.join(img_path, folder_name_vf), exist_ok=True)
        flip_image.save(os.path.join(img_path, folder_name_vf, f"{base_name}_VF.jpg"))

def VFlip_bbox_coordinates(image_height, ymin, ymax):
    return image_height - ymin, image_height - ymax

def xmlVflip(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    image_height = int(root.find('size/height').text)
    for fln in root.iter('filename'):
        original_filename = fln.text
        new_name = f"_VF.jpg"
        modified_filename = original_filename.replace('.jpg', new_name)
        fln.text = modified_filename
        #tree.write(modified_filename)
    for path in root.iter('path'):
        original_path = path.text
        new_name = f"_VF.jpg"
        modified_path = original_path.replace('.jpg', new_name)
        path.text = modified_path
        #tree.write(modified_path)
    for obj in root.iter('object'):
        for bbox in obj.iter('bndbox'):
            ymin = int(bbox.find('ymin').text)
            ymax = int(bbox.find('ymax').text)
            new_ymin, new_ymax = VFlip_bbox_coordinates(image_height, ymin, ymax)
            bbox.find('ymin').text = str(new_ymin)
            bbox.find('ymax').text = str(new_ymax)

    base_name, extension = os.path.splitext(os.path.basename(xml_file))
    new_xml_name = f"{base_name}_VF.xml"
    output_xml_path = os.path.join(img_path, folder_name_vf, new_xml_name)
    tree.write(output_xml_path)

def xmlVflip_all(xml_files):
    for xml_file in xml_files:
        xmlVflip(xml_file)

############################# Rotation ############################

#1. Find new vertices (aka bounding box corners) with respect to old bbox(!) center
#2. Find distance from bbox center and rotated vertices (num. 1)
#3. Find new bbox center with respect to image center
#4. Add distances (num. 2) to new bbox center (num. 3)
def imgRotation(img_files):
    print(f"|**************** aug_rotation 폴더에 저장됩니다.****************|")
    for i in num_rot:
        #print(f"i:{i}")
        for j in range(len(img_files)):
            #print(f"files[j]:{img_files}")
            replace_path = img_files[j].replace("\\", "/")
            image = cv2.imread(replace_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image.shape[:2]
            center_img = (width // 2, height // 2)
            base_name = os.path.basename(replace_path).split('.')[0]
            os.makedirs(os.path.join(img_path, folder_name_rt), exist_ok=True)
            rotate_matrix = cv2.getRotationMatrix2D(center=center_img, angle= i, scale=1)
            rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
            cv2.imwrite(os.path.join(img_path, folder_name_rt, f"{base_name}_RT{i}.jpg"), rotated_image)

def xmlRotation_all(xml_files):
    for xml_file in xml_files:
        for i in num_rot:
            xmlRotation(xml_file, i)
def rotate_vertices(vertices, angle, bbox_center, image_height, image_width):
    # Rotate a point around a given center
    angle_rad = np.radians(- angle)
    x, y = vertices
    cx, cy = bbox_center
    new_x = (((x - cx) * np.cos(angle_rad)) - ((y - cy) * np.sin(angle_rad))) + cx
    new_y = (((x - cx) * np.sin(angle_rad)) + ((y - cy) * np.cos(angle_rad))) + cy
    if new_y < 0:
        new_y = 0
    elif new_y > image_height:
        new_y = image_height
    elif new_x > image_width:
        new_x = image_width
    elif new_x < 0:
        new_x = 0
    return new_x, new_y

def maxNminDistance(rotated_vertices, bbox_center):
    max_x = max(rotated_vertices, key=lambda point: point[0])[0]
    max_y = max(rotated_vertices, key=lambda point: point[1])[1]
    dis_x = max_x - bbox_center[0]
    dis_y = max_y - bbox_center[1]
    return dis_x, dis_y

def rotate_central_point(bbox_center, angle, image_center):
    x, y = bbox_center
    angle_rad = np.radians(360 - angle)
    translated_point = np.array([x - image_center[0], y - image_center[1]])
    rotated_x = (translated_point[0] * np.cos(angle_rad)) - (translated_point[1] * np.sin(angle_rad))
    rotated_y = (translated_point[0] * np.sin(angle_rad)) + (translated_point[1] * np.cos(angle_rad))
    new_x = rotated_x + image_center[0]
    new_y = rotated_y + image_center[1]
    return new_x, new_y

def final_vertices(new_bbox_center, distance_from_center):
    new_xmin = new_bbox_center[0] - distance_from_center[0]
    new_ymin = new_bbox_center[1] - distance_from_center[1]
    new_xmax = new_bbox_center[0] + distance_from_center[0]
    new_ymax = new_bbox_center[1] + distance_from_center[1]
    return (new_xmin, new_ymin, new_xmax, new_ymax)

def move_and_rotate_box(box_vertices, i, image_center, bbox_center, image_height, image_width):
    rotated_vertices = [rotate_vertices(vertex, i, bbox_center, image_height, image_width) for vertex in box_vertices]
    #print(f"rotated_vertices:{rotated_vertices}")
    #[(544.8993633237616, 471.94317075434975), (666.8807821328413, 474.0723643396983), (665.1006366762384, 576.0568292456503), (543.1192178671587, 573.9276356603017)]
    distance_from_center = maxNminDistance(rotated_vertices, bbox_center)
    #print(f"distance_from_center:{distance_from_center}")
    new_bbox_center = rotate_central_point(bbox_center, i, image_center)
    #print(f"new_bbox_center:{new_bbox_center}")
    #(584.0646959630676, 474.3218169899218))
    final_vertices_new_bbox = final_vertices(new_bbox_center, distance_from_center)
    return final_vertices_new_bbox

def xmlRotation(xml_file, i):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    image_height = int(root.find('size/height').text)
    image_width = int(root.find('size/width').text)
    image_center = np.array([image_width / 2, image_height / 2])
    for fln in root.iter('filename'):
        original_filename = fln.text
        new_name = f"_RT{i}.jpg"
        modified_filename = original_filename.replace('.jpg', new_name)
        fln.text = modified_filename
        # tree.write(modified_filename)
    for path in root.iter('path'):
        original_path = path.text
        new_name = f"_RT{i}.jpg"
        modified_path = original_path.replace('.jpg', new_name)
        path.text = modified_path
    for obj in root.iter('object'):
        for bbox in obj.iter('bndbox'):
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            corners.append(xmin)
            corners.append(ymin)
            corners.append(xmax)
            corners.append(ymax)
            box_vertices = np.array([[corners[0], corners[1]], [corners[2], corners[1]], [corners[2], corners[3]],
                                     [corners[0], corners[3]]])
            #print(f"box_vertices:{box_vertices}")
            bbox_center = np.mean(box_vertices, axis=0)
            #print(f"bbox_center:{bbox_center}")
            result_vertices = move_and_rotate_box(box_vertices, i, image_center, bbox_center, image_height, image_width)
            #print(f"result_vertices:{result_vertices}")
            min_x = result_vertices[0]
            min_y = result_vertices[1]
            max_x = result_vertices[2]
            max_y = result_vertices[3]

            bbox.find('xmin').text = str(min_x)
            bbox.find('ymin').text = str(min_y)
            bbox.find('xmax').text = str(max_x)
            bbox.find('ymax').text = str(max_y)
    base_name, extension = os.path.splitext(os.path.basename(xml_file))
    new_xml_name = f"{base_name}_RT{i}.xml"
    output_xml_path = os.path.join(img_path, folder_name_rt, new_xml_name)
    tree.write(output_xml_path)
#####################################################################

if choice_option == str(1):
    imgHshift(img_files)
    xmlHshift_all(xml_files, num_shift)

if choice_option == str(2):
    imgVshift(img_files)
    xmlVshift_all(xml_files, num_shift)

if choice_option == str(3):
    imgHflip(img_files)
    xmlHflip_all(xml_files)

if choice_option == str(4):
    imgVflip(img_files)
    xmlVflip_all(xml_files)

if choice_option == str(5):
    imgRotation(img_files)
    xmlRotation_all(xml_files)