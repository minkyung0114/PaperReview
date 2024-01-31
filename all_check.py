import os, glob
import xml.etree.ElementTree as ET
import re
path = r'D:\AI_SVT_Training_mk\annotations\annos'
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
  return classes_names, file_names

classes,file_names = make_PBTXTnNAME(path)

def removeNoneClassName():
    xmlDir = r"D:\AI_SVT_Training_mk\annotations\annos"
    xmlDir = xmlDir.replace(r"\\", r"/")
    file_list = os.listdir(xmlDir)
    xml_list = []
    for file in file_list:
        if '.xml' in file:
            xml_list.append(file)

    for xml_file in xml_list:
        target_path = os.path.join(xmlDir, xml_file)
        #print(f"target_path:{target_path}")
        targetXML = open(target_path, 'rt', encoding='utf-8')
        tree = ET.parse(targetXML)
        root = tree.getroot()
        target_tag = root.find("object")
        # print(f"target_tag:{target_tag}")

        if target_tag is None:
            targetXML.close()
            os.remove(target_path)


def matching():
    FILE_PATH = 'D:/AI_SVT_Training_mk/annotations/annos'
    files = os.listdir(FILE_PATH)
    files.sort()

    xmls = [file.split('.xml')[0] for file in files if file.endswith('.xml')]
    jpgs = [file.split('.jpg')[0] for file in files if file.endswith('.jpg' or '.JPG')]
    print(f"========================================")
    print(f"xmls:{len(xmls)}")
    print(f"jpgs:{len(jpgs)}")
    print(f"========================================")
    if len(jpgs) > len(xmls):
        intersection = list(set(jpgs) - set(xmls))

        for i in range(len(intersection)):
            file = intersection[i] + '.jpg'
            print(f"file:{file}")
            os.remove(os.path.join(FILE_PATH, file))

    else:
        intersection = list(set(xmls) - set(jpgs))
        for i in range(len(intersection)):
            file = intersection[i] + '.xml'
            print(f"file:{file}")
            os.remove(os.path.join(FILE_PATH, file))

    print(f"intersection:{len(intersection)}")
    print(f"삭제완료")
    print(f"===============================")

def changeClassNum():
    config_file_path = r"D:\AI_SVT_Training_mk\configs\test.config"
    config_file_path = config_file_path.replace("\\", "/")
    num_classes = len(classes)
    if num_classes:
        # Read the content of the ".config" file
        with open(config_file_path, "r") as config_file:
            config_content = config_file.read()

        # Define a regular expression pattern to match the class_num line
        pattern = r"num_classes:\d+"

        # Use re.sub to replace all matched instances of class_num
        new_config_content = re.sub(pattern, f"num_classes:{num_classes}", config_content)

        # Write the modified content back to the ".config" file
        with open(config_file_path, "w") as config_file:
            config_file.write(new_config_content)
    else:
        print("Invalid input. Please enter a single digit.")


if __name__ == "__main__":
    removeNoneClassName()
    matching()

with open(label_map_path, "w",encoding='utf-8') as a:
    for i, class_name in enumerate(classes, 1):
        print(f"ID:{i}, class_name:{class_name}")
        pbtxt_content = f"item {{ \n id: {i}\n name:'{class_name}'\n display_name:'{class_name}'\n}}\n"

print(f"classes = {len(classes)}")
print(f'*********************************Successfully created label_map.pbtxt*********************************')

user_input = input(f"Change number of class in CONFIG file (y/n): ")
if user_input.lower() == 'y':
        changeClassNum()