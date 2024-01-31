#-*- coding: utf-8 -*-
import os, glob
import xml.etree.ElementTree as ET


print(f" 폴더경로를 입력하세요")
FILE_PATH = input()
files = os.listdir(FILE_PATH)
files.sort()


xmls = [file.split('.xml')[0] for file in files if file.endswith('.xml')]
xml_list = [file for file in files if file.endswith('.xml')]
jpgs = [file.split('.jpg')[0] for file in files if file.endswith('.jpg' or '.JPG')]
print(f"*********************************************************")
print(f"xmls 갯수:{len(xmls)}")
print(f"jpgs 갯수:{len(jpgs)}")
print(f"*********************************************************")
#print(f"xml_list{xml_list}")
remove_list = []

if len(jpgs) > len(xmls):
    intersection = list(set(jpgs) - set(xmls))

    for i in range (len(intersection)):
        file = intersection[i]+'.jpg'
        print(f"file:{file}")
        os.remove(os.path.join(FILE_PATH,file))

    #['spot_B15_R4', 'spot_B15_R6', 'spot_B15_R5_Vf67', 'spot_B15_R6_Vf68', 'spot_B15_R4_Vf66', 'spot_B15_R5']

else :
    intersection = list(set(xmls) - set(jpgs))
    for i in range (len(intersection)):
        file = intersection[i]+'.xml'
        print(f"file:{file}")
        os.remove(os.path.join(FILE_PATH,file))

print(f"intersection:{intersection}")

if len(intersection) != 0:
    print(f"============================")
    print(f"삭제완료")
    print(f"============================")

        
else:
    print(f"================ jpg, xml pair맞음 , | 삭제할 것 없음================")
        

for xml_file in xml_list:
    #print(f"xml list:{xml_list}")
    #['H15_add_filterScratch1_R1.xml', 'H15_add_filterScratch1_R101.xml',
    target_path = os.path.join(FILE_PATH, xml_file)
    #print(f"target_path:{target_path}")
    #D:\AI_SVT_Training_mk\annotations\annos\H15_add_filterScratch1_R1.xml
    targetXML = open(target_path, 'rt', encoding='utf-8')
    tree = ET.parse(targetXML)
    root = tree.getroot()
    #print(f"root:{root}")

    filename = root.find("filename")
    filename = filename.text
    filename_path = os.path.join(FILE_PATH,filename)
    #print(f"filename_path:{filename_path}")

    object = root.find('object')
    #object = object.text
    #print(f"object:{object}")

    if object is None:
        remove_list.append(os.path.join(FILE_PATH, xml_file))
        remove_list.append(os.path.join(FILE_PATH, filename))


print(f"===================================")
print(f"remove_list 갯수 :{len(remove_list)}")
print(f"===================================")

if len(remove_list) != 0:

    for idx, file_list in enumerate(remove_list):

        os.remove(file_list)
    print(f"--=======BBOX 안그려진 파일 삭제완료!=======--")
else:
    print(f"--=======BBOX 안그려진 삭제할 파일 없음!=======--")
