import os, glob
from PIL import Image
import PIL.ImageOps
print(f"경로입력하세요")

#INVERT_IMG_PATH = r'D:/AI_SVT_Training_mk/annotations/annos/convert_img'
INVERT_IMG_PATH = input()

#IMG_PATH = r'D:/AI_SVT_Training_mk/annotations/annos'
IMG_PATH = os.path.join(INVERT_IMG_PATH,F"invertIMG")

os.makedirs(IMG_PATH, exist_ok=True)

for i in glob.glob(os.path.join(INVERT_IMG_PATH,'*.jpg' or '*.bmp')):
    #print(f"path : {i}")
    base_name = i.split('\\')[-1]
    #print(f"basename = {base_name}")
    new_name = base_name.split('.')[0]
    #print(f"new_name = {new_name}")
    new_name = new_name + '_iv.jpg'
    #print(f"new_name = {new_name}")
    name_name1 = f'{IMG_PATH}/{new_name}'
    print(f"new_name1 = {name_name1}")
    image = Image.open(i)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(name_name1)

