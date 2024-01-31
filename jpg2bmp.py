import glob
from PIL import Image
import os
from tqdm import tqdm

print(f"마지막 \를 제외하고 경로입력하세요!")
src_path = str(input())
dst_path = os.path.join(src_path,"bmp_images/") #bmp images path

if not os.path.isdir(dst_path): # make dst dir if it's not existed
    os.mkdir(dst_path)

src_path_jpg = (img for img in set(glob.glob(src_path+"/*.jpg" or src_path+"/*.JPG")))

for img in tqdm(src_path_jpg):

    images = Image.open(img)

    name = img.split("\\")[-1]
    name = name.split(".")[0]+".bmp"
    new_name = os.path.join(dst_path,name)
    new_name = new_name.replace("\\","/")

    images.save(new_name)

print(f"it's done.")