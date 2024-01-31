

import cv2,os
import numpy as np

from PIL import Image
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree,dump

print(f" 라벨링 파일이 들어있는 [전체 폴더경로]를 입력하세요.")
dataDir = input()


print(f"######################################################")
print(f"######################################################")




file_list = os.listdir(dataDir)

xml_list = []
img_list = []
new_xml_list=[]

save_path = file_list



for file in file_list:

    if file.endswith('jpg' or '.JPG'):
        img_list.append(file)
        img_list.sort()


    elif file.endswith('xml'):
        xml_list.append(file)
        xml_list.sort()

#print(f"img_list:{img_list}")
#print(f"xml_list:{xml_list}")


def indent(elem, level=0): #자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def xml_2img(xml_list,indent):
    for idx, xml in enumerate(xml_list):

        target_width = 1280
        target_height = 960
        ori_width = 2448
        ori_height = 2048
        x_scale = target_width / ori_width
        y_scale = target_height / ori_height

        if idx % 2 == 0:

            xml_path1 = xml_list[idx]
            xml_path2 = xml_list[idx+1]
            xml_targetPath1 = os.path.join(dataDir, xml_path1)
            targetXML1 = open(xml_targetPath1, 'rt', encoding='UTF8')

            xml_targetPath1 = os.path.join(dataDir, xml_path1)

            tree1 = ET.parse(targetXML1)
            root1 = tree1.getroot()

            folder = root1.find('folder').text
            filename = root1.find('filename').text
            path = root1.find('path').text
            segmented = root1.find('segmented').text

            # print(f"folder:{folder}")
            # print(f"filename:{filename}")
            # print(f"path:{path}")
            # print(f"segmented:{segmented}")

            # 새로 xml을 만들기
            root = Element('annotation')
            SubElement(root, 'folder').text = folder
            SubElement(root, 'filename').text = filename
            SubElement(root, 'path').text = path
            source = SubElement(root, 'source')
            SubElement(source, 'database').text = 'Unknown'

            size = SubElement(root, 'size')
            SubElement(root, 'segmented').text = segmented

            for xml_size in root1.iter('size'):
                # width = xml_size.find('width').text
                # print(f"width :{width}")2448
                # height = xml_size.find('height').text
                width = '1280'
                height = '960'

                depth = xml_size.find('depth').text

                SubElement(size, 'width').text = str(width)
                SubElement(size, 'height').text = str(height)
                SubElement(size, 'depth').text = depth

            for object1 in root1.iter('object'):
                name = object1.find('name').text
                pose = object1.find('pose').text
                truncated = object1.find('truncated').text
                difficult = object1.find('difficult').text

                xmin = int(object1.find('bndbox')[0].text)
                xmin = int(xmin * x_scale)-640

                ymin = int(object1.find('bndbox')[1].text)
                ymin = int(ymin * y_scale)

                xmax = int(object1.find('bndbox')[2].text)
                xmax = int(xmax * x_scale)-640

                ymax = int(object1.find('bndbox')[3].text)
                ymax = int(ymax * y_scale)
                # print(f"ymin1:{ymin}")

                obj = SubElement(root, 'object')
                SubElement(obj, 'name').text = name
                SubElement(obj, 'pose').text = pose
                SubElement(obj, 'truncated').text = truncated
                SubElement(obj, 'difficult').text = difficult
                bbox = SubElement(obj, 'bndbox')
                SubElement(bbox, 'xmin').text = str(xmin)
                SubElement(bbox, 'ymin').text = str(ymin)
                SubElement(bbox, 'xmax').text = str(xmax)
                SubElement(bbox, 'ymax').text = str(ymax)

            xml_targetPath2 = os.path.join(dataDir, xml_path2)

            targetXML2 = open(xml_targetPath2, 'rt', encoding='UTF8')
            tree2 = ET.parse(targetXML2)
            root2 = tree2.getroot()

            for object2 in root2.iter('object'):
                name = object2.find('name').text
                pose = object2.find('pose').text
                truncated = object2.find('truncated').text
                difficult = object2.find('difficult').text

                xmin = int(object2.find('bndbox')[0].text)
                xmin = int(xmin * x_scale)
                xmin = int(xmin * x_scale)+ 640

                ymin = int(object2.find('bndbox')[1].text)
                ymin = int(ymin * y_scale)

                xmax = int(object2.find('bndbox')[2].text)
                xmax = int(xmax * x_scale)
                xmax = int(xmax * x_scale)+ 640

                ymax = int(object2.find('bndbox')[3].text)
                ymax = int(ymax * y_scale)

                obj2 = SubElement(root, 'object')
                SubElement(obj2, 'name').text = name
                SubElement(obj2, 'pose').text = pose
                SubElement(obj2, 'truncated').text = truncated
                SubElement(obj2, 'difficult').text = difficult
                bbox2 = SubElement(obj2, 'bndbox')
                SubElement(bbox2, 'xmin').text = str(xmin)
                SubElement(bbox2, 'ymin').text = str(ymin)
                SubElement(bbox2, 'xmax').text = str(xmax)
                SubElement(bbox2, 'ymax').text = str(ymax)

            indent(root)
            tree = ElementTree(root)
            tree.write(xml_targetPath1)



def xml_img(xml_list,indent):
    for idx, xml in enumerate(xml_list):

        target_width = 1280
        target_height = 960
        ori_width = 2448
        ori_height = 2048
        x_scale = target_width / ori_width
        y_scale = target_height / ori_height



        xml_path1 = xml_list[idx]
        xml_targetPath1 = os.path.join(dataDir, xml_path1)
        targetXML1 = open(xml_targetPath1, 'rt', encoding='UTF8')

        xml_targetPath1 = os.path.join(dataDir, xml_path1)

        tree1 = ET.parse(targetXML1)
        root1 = tree1.getroot()

        folder = root1.find('folder').text
        filename = root1.find('filename').text
        path = root1.find('path').text
        segmented = root1.find('segmented').text

        # print(f"folder:{folder}")
        # print(f"filename:{filename}")
        # print(f"path:{path}")
        # print(f"segmented:{segmented}")

        # 새로 xml을 만들기
        root = Element('annotation')
        SubElement(root, 'folder').text = folder
        SubElement(root, 'filename').text = filename
        SubElement(root, 'path').text = path
        source = SubElement(root, 'source')
        SubElement(source, 'database').text = 'Unknown'

        size = SubElement(root, 'size')
        SubElement(root, 'segmented').text = segmented

        for xml_size in root1.iter('size'):
            # width = xml_size.find('width').text
            # print(f"width :{width}")2448
            # height = xml_size.find('height').text
            width = '1280'
            height = '960'

            depth = xml_size.find('depth').text

            SubElement(size, 'width').text = str(width)
            SubElement(size, 'height').text = str(height)
            SubElement(size, 'depth').text = depth

        for object1 in root1.iter('object'):
            name = object1.find('name').text
            pose = object1.find('pose').text
            truncated = object1.find('truncated').text
            difficult = object1.find('difficult').text

            xmin = int(object1.find('bndbox')[0].text)
            xmin = int(xmin * x_scale)

            ymin = int(object1.find('bndbox')[1].text)
            ymin = int(ymin * y_scale)

            xmax = int(object1.find('bndbox')[2].text)
            xmax = int(xmax * x_scale)

            ymax = int(object1.find('bndbox')[3].text)
            ymax = int(ymax * y_scale)
            # print(f"ymin1:{ymin}")

            obj = SubElement(root, 'object')
            SubElement(obj, 'name').text = name
            SubElement(obj, 'pose').text = pose
            SubElement(obj, 'truncated').text = truncated
            SubElement(obj, 'difficult').text = difficult
            bbox = SubElement(obj, 'bndbox')
            SubElement(bbox, 'xmin').text = str(xmin)
            SubElement(bbox, 'ymin').text = str(ymin)
            SubElement(bbox, 'xmax').text = str(xmax)
            SubElement(bbox, 'ymax').text = str(ymax)


        indent(root)
        tree = ElementTree(root)
        tree.write(xml_targetPath1)

xml_img(xml_list,indent)

def merge_2img(img_list):


    target_width =1280/2
    #960
    target_height=960


    for idx, img in enumerate(img_list):

        if idx%2 == 0:

            image_path1 = img_list[idx]
            image_path2 = img_list[idx+1]
            img_path1 = os.path.join(dataDir,image_path1)
            #print(f"img_path:{img_path1}")
            img1 = Image.open(img_path1)
            img1_w, img1_h = img1.size
            img1_wscale = target_width / img1_w
            #print(f"img1_wscale:{img1_wscale}")
            img1_hscale = target_height /img1_h
            img1_w = int(img1_w * img1_wscale)
            img1_h = int(img1_h * img1_hscale)
            #print(f"img1_w:{img1_w},img1_h:{img1_h}")
            img1 = img1.resize((img1_w,img1_h))
            #print(f"img11 size: {img1.size}")

            #image1_size  = img1.size

            img_path2 = os.path.join(dataDir,image_path2)
            img2 = Image.open(img_path2)
            #image2_size = img2.size
            img2_w, img2_h = img2.size

            img2_wscale = target_width /img2_w
            img2_hscale = target_height / img2_h
            img2_w = int(img2_w * img2_wscale)
            img2_h = int(img2_h * img2_hscale)

            print(f"img2_w:{img2_w},img2_h:{img2_h}")

            img2 = img2.resize((img2_w, img2_h))


            #w,h

            #new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            new_image = Image.new('RGB',(int(target_width*2), int(target_height)), (250,250,250))

            new_image.paste(img1, (0, 0))
            new_image.paste(img2, (img1_w, 0))
            #new_image.resize((target_width,target_height))
            new_image.save(os.path.join(img_path1))




#merge_2img(img_list)



def merge_img(img_list):

    target_width =1280
    #960
    target_height=960


    for idx, img in enumerate(img_list):



        image_path1 = img_list[idx]
        img_path1 = os.path.join(dataDir,image_path1)
        #print(f"img_path:{img_path1}")
        img1 = Image.open(img_path1)
        img1_w, img1_h = img1.size
        img1_wscale = target_width / img1_w
        #print(f"img1_wscale:{img1_wscale}")
        img1_hscale = target_height /img1_h
        img1_w = int(img1_w * img1_wscale)
        img1_h = int(img1_h * img1_hscale)
        #print(f"img1_w:{img1_w},img1_h:{img1_h}")
        img1 = img1.resize((img1_w,img1_h))
        #print(f"img11 size: {img1.size}")


        #new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
        new_image = Image.new('RGB',(int(target_width), int(target_height)), (250,250,250))

        new_image.paste(img1, (0, 0))
        #new_image.resize((target_width,target_height))
        new_image.save(os.path.join(img_path1))




merge_img(img_list)