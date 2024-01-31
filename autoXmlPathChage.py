#-*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

print(f"=========================")
print(f"자동으로 폴더 변경 수정합니다.")
print(f"=========================")
print(f"현재 라벨링된 xml파일이 포함된 폴더경로를 입력해주세요")
xmlDir = input()
xmlDir= xmlDir.replace(r"\\",r"/")

file_list = os.listdir(xmlDir)
#print(f"file_list:{file_list}")
xml_list = []
for file in file_list:
    if '.xml' in file:
        xml_list.append(file)


def changeFolder(xml_list):
    print(f"##################")
    print(f" 폴더명 annos 변경시작 .")
    print(f"##################")

    modi_FolderName = f"annos"

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        #print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        ##수정할 부분
        target_tag = root.find("folder")
        original = target_tag.text  # 원본 String

        # print(f"original:{original}")
        modified = original.replace(original, modi_FolderName)
        target_tag.text = modified

        tree.write(target_path)




def changePath(xml_list):
    #print(f" xmlDir")
    #origin_path = xmlDir
    #print(f"origin_path:{origin_path}")
    #origin_path = origin_path.split('\\')
    #origin_path = origin_path
    #print(f"origin_path:{origin_path}")
    #print(f" path 수정할 경로 입력.")
    modi_path = r"D:\AI_SVT_Training_mk\annotations\annos"

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        #print(f"target_path:{target_path}")
        origin_path = os.path.dirname(target_path)
        print(f"origin_path:{origin_path}")

        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        ##수정할 부분
        target_tag = root.find("path")
        original = target_tag.text  # 원본 String
        # original = target_tag.text  # 원본 String
        # print(f"original:{original}")
        modified = original.replace(origin_path, modi_path)
        print(f"modified:{modified}")
        target_tag.text = modified

        tree.write(target_path)




print(f"===================================================")
print(f" D:/AI_SVT_Training_mk/annotations/annos 경로 설정됨.")
print(f"===================================================")




def changeClassName(xml_list):

    print(f"###############################")
    print(f" origin 라벨링 class name 입력하기.")
    print(f"###############################")
    original_fileName = str(input())
    print(f"===============================")
    print(f"###############################")
    print(f" 수정할 라벨링  class name 입력하기.")
    print(f"###############################")

    modi_fileName = str(input())

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='utf-8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        print(f"root:{root}")

        for obj in root.iter('object'):

            class_name = obj.find('name')
            original  = class_name.text
            modified = original.replace(original_fileName, modi_fileName)
            class_name.text = modified
            #print(f"class_name:{class_name.text}")
            '''
            box 바꾸고 싶으면 이렇게 하면됨 
            obj.find('bndbox')[3].text = 100
            obj.find('bndbox')[2].text = 100
            obj.find('bndbox')[1].text = 10                 
            obj.find('bndbox')[0].text = 10
                 '''
        tree.write(target_path)


changePath(xml_list)


