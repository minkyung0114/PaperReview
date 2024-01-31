#-*- coding: utf-8 -*-
import os
import glob
import xml.etree.ElementTree as ET
from tqdm import tqdm
#print(os.listdir())
#path = r'./annotations/annos'
print(f"==============")
print(f"폴더 경로입력하세요")
print(f"==============")


path=str(input())

label_map_path = os.path.join("./label_map.pbtxt")
file_path = os.path.join("./annotations/train.txt")


def make_PBTXTnNAME(path):
  classes_names = []
  file_names= []

  for xml_file in glob.glob(path + '/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
        classes_names.append(member[0].text)

    for name in root.findall('filename'):
        name = name.text.split('.')[0]
        file_names.append(name)

  classes_names = list(set(classes_names))
  classes_names.sort()
  file_names.sort()
  
  #print(f"classes_names;{classes_names}")
  #print(f"file_names;{file_names}")


  return classes_names, file_names

classes,file_names = make_PBTXTnNAME(path)
print(f"===============================")
print(f"file names = {len(file_names)}")
print(f"===============================")
print(f"===============================")
print(f"classes = {len(classes)}")
print(f"===============================")



with open(label_map_path, "w",encoding='utf-8') as a:

    for i, class_name in enumerate(classes, 1):


        print(f"===============================")
        print(f"ID:{i}, class_name:{class_name}")
        pbtxt_content = f"item {{ \n id: {i}\n name:'{class_name}'\n display_name:'{class_name}'\n}}\n"
        #pbtxt_content = pbtxt_content.strip()
        #print(f"pbtxt_content:{pbtxt_content}")
        #a.write(pbtxt_content)
print(f'*********************************Successfully created label_map.pbtxt*********************************')


'''
with open(file_path, "w",encoding='utf-8') as f:
    f.writelines('\n'.join(file_names))
    print(f'*********************************Successfully created train.txt*********************************')
 
'''