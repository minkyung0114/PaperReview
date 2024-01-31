# -*- coding: utf-8 -*-
import glob
from PIL import Image
import os
from tqdm import tqdm
import time
import shutil

print(f"마지막 \를 제외하고 경로입력하세요!")
src_path = str(input())   # bmp images path
dst_path = os.path.join(src_path,"jpg_images/") #jpg images path

if not os.path.isdir(dst_path): # make dst dir if it's not existed
    os.mkdir(dst_path)

bmp_path = os.path.join(src_path,'bmp_images/')
os.makedirs(bmp_path, exist_ok=True)

src_path_bmp = (img for img in set(glob.glob(src_path+"/*.bmp" or src_path+"/*.BMP")))
#bmpfiles=[img for img in set(glob.glob(src_path+"/*.bmp" or src_path+"/*.BMP"))]

for img in tqdm(src_path_bmp, desc='iterate list'):
    time.sleep(0.1)

    images = Image.open(img)

    name = img.split("\\")[-1]
    name = name.split(".")[0]+".jpg"
    new_name = os.path.join(dst_path,name)
    new_name = new_name.replace("\\","/")

    images.save(new_name)
    images.close()
 
for img in set(glob.glob(src_path+"/*.bmp" or src_path+"/*.BMP")):
    img = img.replace("\\","/")
    print(f"file:{img}")
    shutil.move(img,bmp_path)

    
