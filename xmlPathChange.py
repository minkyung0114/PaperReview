#-*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET


print(f"원하는 것을 선택하세요 ")
print(f"1.<folder>변경  2.<file name> 변경 3.<path> 변경 4.class 라벨 name변경" )
print(f"5. 특정클래스명 삭제 6 path경로 확인 7 비어있는 클래스 파일삭제 8. depth변경 9.depth확인")
choice_option = str(input())


print(f" xml파일이 들어있는 [전체 폴더경로]를 입력하세요.")
#xmlDir = r"D:\AI_SVT_Training\images"
xmlDir = input()
#xmlDir = r"D:\AI_SVT_Training_mk\annotations\annos"

xmlDir= xmlDir.replace(r"\\",r"/")
#print(f" D:\AI_SVT_Training_mk\annotations\annos 경로 설정됨.")

##targetDir에서 .xml파일 이름들 리스트로 가져오기
file_list = os.listdir(xmlDir)
xml_list = []
for file in file_list:
    if '.xml' in file:
        xml_list.append(file)


        
def confPath(xml_list):
    
   
    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        #print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        ##수정할 부분
        target_tag = root.find("path")
        original = target_tag.text  # 원본 String
        #original = target_tag.text  # 원본 String
        print(f"original path :{original}")

        
       
def changedapth(xml_list):
    
   
    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        #print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        modi_fileName="3"

        for obj in root.iter('size'):

            depth_name = obj.find('depth')
            original = depth_name.text     
            if original == f"1":

                modified = original.replace(original, modi_fileName)
                depth_name.text = modified



        tree.write(target_path)
        print(f"depth확인 : {depth_name.text}")


def confdapth(xml_list):
    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        # print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        modi_fileName = 3

        for obj in root.iter('size'):

            depth_name = obj.find('depth')
            print(f"depth확인 : {depth_name.text}")
                
   
        

        
        
def changePath(xml_list):
    
    print(f" path 수정하고싶은 경로 입력.<path>제외")
    origin_path = str(input())
    print(f" path 수정할 경로 입력.")
    modi_path = str(input())

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        ##수정할 부분
        target_tag = root.find("path")
        original = target_tag.text  # 원본 String
        #original = target_tag.text  # 원본 String
        #print(f"original:{original}")
        modified = original.replace(origin_path, modi_path)
        target_tag.text = modified

        tree.write(target_path)
        


def changeFolder(xml_list):

    print(f"##################")
    print(f" 수정할 폴더명 입력.")
    print(f"##################")


    modi_FolderName = str(input())


    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
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

def changeFilename(xml_list):

    print(f"##################")
    print(f" 수정할 파일이름 부분 입력.")
    print(f" origin 입력_확장자입력하면도움됨")
    print(f"##################")   
    
    
    ori_fileName= str(input())
    print(f" 수정할 파일 이름 부분 입력.")
    modi_fileName = str(input())
    

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='UTF8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        ##수정할 부분
        target_tag = root.find("filename")
        original = target_tag.text  # 원본 String
        # print(f"original:{original}")

        modified = original.replace(ori_fileName, modi_fileName)
        target_tag.text = modified

        tree.write(target_path)
        
    

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
            original = class_name.text
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

def removeClassName(xml_list):

    print(f"###############################")
    print(f" 삭제할 클래스명 입력하기.")
    remove_fileName = str(input())
    print(f"###############################")

    print(f"===============================")

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='utf-8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        #print(f"root:{root}")


        for obj in root.iter('object'):

            class_name = obj.find('name')
            origin_name = class_name.text
            if origin_name == remove_fileName:

                root.remove(obj)

        tree.write(target_path)

def removeNoneClassName(xml_list):

    print(f"###############################")
    print(f" 비어있는 클래스명 파일삭제 시작.")
    print(f"###############################")
    print(f"===============================")



    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='utf-8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        target_tag = root.find("object")
        #print(f"target_tag:{target_tag}")
        

        if target_tag is None:
            targetXML.close()
            os.remove(target_path)
            
            

        
            







if choice_option == str(1):
    changeFolder(xml_list)

elif choice_option == str(2):
    changeFilename(xml_list)

elif choice_option == str(3):
    changePath(xml_list)

elif choice_option == str(4):
    changeClassName(xml_list)


elif choice_option == str(5):
    removeClassName(xml_list)

elif choice_option == str(6):
   confPath(xml_list)
elif choice_option == str(7):
   removeNoneClassName(xml_list)
   
elif choice_option == str(8):
   changedapth(xml_list)

elif choice_option == str(9):
   confdapth(xml_list)
print(f"It's done.")