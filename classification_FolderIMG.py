#-*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
from PIL import Image

'''
xml파일에서 클래스 별로 classification폴더별로 나눠서 이미지 저장 
'''
print(f" xml파일이 들어있는 [전체 폴더경로]를 입력하세요.")

xmlDir = input()
xmlDir= xmlDir.replace(r"\\",r"/")

file_list = os.listdir(xmlDir)
xml_list = []
for file in file_list:
    if '.xml' in file:
        xml_list.append(file)

for xml_file in xml_list:


    target_path = os.path.join(xmlDir, xml_file)
    print(f"target_path:{target_path}")
    targetXML = open(target_path, 'rt', encoding='utf-8')
    tree = ET.parse(targetXML)
    root = tree.getroot()

    target_tag = root.find("path")
    original = target_tag.text  # 원본 String
    print(f"original:{original}")


    for obj in root.iter('object'):

        class_name = obj.find('name')
        print(f"class name :{class_name.text }")

        if class_name.text == "1":
            folder1 = os.makedirs(os.path.join(xmlDir,'1'),exist_ok=True)
            images = Image.open(original)
            name = original.split("\\")[-1]
            save_imgpath1 = os.path.join(xmlDir,'1',name)
            images.save(os.path.join(save_imgpath1))

        elif class_name.text == "2":
            folder2 = os.makedirs(os.path.join(xmlDir,'2'),exist_ok=True)
            images = Image.open(original)
            name = original.split("\\")[-1]
            save_imgpath2 = os.path.join(xmlDir,'2',name)
            images.save(os.path.join(save_imgpath2))

        elif class_name.text == "3":
            folder3 = os.makedirs(os.path.join(xmlDir,'3'),exist_ok=True)
            images = Image.open(original)
            name = original.split("\\")[-1]
            save_imgpath3 = os.path.join(xmlDir,'3',name)
            images.save(os.path.join(save_imgpath3))




print(f"It's done.")