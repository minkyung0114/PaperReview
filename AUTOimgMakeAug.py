# -*- encoding: utf-8 -*-
import os,glob,sys, random
from PIL import Image, ImageEnhance, ImageChops
import tqdm
import time
import shutil
print(sys.getdefaultencoding())

print(f"이미지 경로입력하세요(마지막 \를 제외)!")
img_path = str(input())


dst_path = os.path.join(img_path,"jpg_images/")
os.makedirs(dst_path,exist_ok=True)
bmp_path = os.path.join(img_path,'bmp_images/')
os.makedirs(bmp_path, exist_ok=True)

src_path_bmp = (img for img in set(glob.glob(img_path+"/*.bmp" or img_path+"/*.BMP")))

for img in tqdm.tqdm(src_path_bmp):
    time.sleep(0.1)

    images = Image.open(img)

    name = img.split("\\")[-1]
    name = name.split(".")[0]+".jpg"
    new_name = os.path.join(dst_path,name)
    new_name = new_name.replace("\\","/")

    images.save(new_name)
    images.close()


jpg_files = glob.glob(dst_path + '/*.jpg' or '/*.JPG')

#print(f"jpg_files:{jpg_files}")

def imgShiftHs(files):
    print(f"|**************** aug_shift폴더에 저장됩니다.****************|")
    folder_name = str("aug_shiftHs")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        #print(f"replace_path:{replace_path}")
        image = Image.open(replace_path)
        image = image.convert('RGB')

        width, height = image.size
        base_name = os.path.basename(replace_path).split('.')[0]

        shift = random.randint(0, width * 0.5)
        horizonal_shift_image = ImageChops.offset(image, shift, 0)
        horizonal_shift_image.paste((0), (0, 0, shift, height))
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        horizonal_shift_image.save(os.path.join(dst_path, folder_name, f"{base_name}_Hs{idx}.jpg"))
    print(f"================================OK================================")


def imgShiftVs(files):
    print(f"|**************** aug_shift폴더에 저장됩니다.****************|")
    folder_name = str("aug_shiftVs")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        image = image.convert('RGB')

        width, height = image.size
        base_name = os.path.basename(replace_path).split('.')[0]

        width, height = image.size

        shift = random.randint(0, height * 0.5)
        vertical_shift_image = ImageChops.offset(image, shift, 0)
        vertical_shift_image.paste((0), (0, 0, width, shift))
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        vertical_shift_image.save(os.path.join(dst_path, folder_name, f"{base_name}_Vh{idx}.jpg"))
    print(f"================================OK================================")





def imgRotate35(files):
    print(f"|**************** aug_rt폴더에 저장됩니다.****************|")
    print(f"360도 기준")
    folder_name = str("aug_rt")


    for idx, file in enumerate(files):

        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        # print(base_name)

        for i in range(1, 360, 35):
            rotate_image = image.rotate(i)  # 시계방향 35도 회전
            print(f"rotate_image:{rotate_image}")
            # rotate_image = image.rotate(rotate_num * i) #시계방향 35도 회전
            os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
            rotate_image.save(os.path.join(dst_path, folder_name, f"{base_name}_R{i}.jpg"))
    print(f"================================OK================================")


def imgFlip_left2right(files):
    print(f"|**************** aug_h_flip 폴더에 저장됩니다.****************|")
    folder_name = str("aug_Hflip")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        flip_image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(dst_path, folder_name, f"{base_name}_Hf{idx}.jpg"))
    print(f"================================OK================================")


def imgFlip_top2bottom(files):
    print(f"|**************** aug_v_flip 폴더에 저장됩니다.****************|")
    folder_name = str("aug_Vflip")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]

        flip_image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(dst_path, folder_name, f"{base_name}_Vf{idx}.jpg"))
    print(f"================================OK================================")



def img_contrast(files):
    print(f"|**************** img_contrast 폴더에 저장됩니다.****************|")
    folder_name = str("aug_contrast")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        enhancer = ImageEnhance.Sharpness(image)
        enhancer = enhancer.enhance(1.8)
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        enhancer.save(os.path.join(dst_path, folder_name, f"{base_name}_Aug_enhancer_{idx}.jpg"))
    print(f"================================OK================================")


def img_brightness(files):
    print(f"|**************** img_contrast 폴더에 저장됩니다.****************|")
    folder_name = str("aug_brightness")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        enhancer = ImageEnhance.Brightness(image)
        enhancer = enhancer.enhance(1.5)
        os.makedirs(os.path.join(dst_path, folder_name), exist_ok=True)
        enhancer.save(os.path.join(dst_path, folder_name, f"{base_name}_Aug_brightness_{idx}.jpg"))
    print(f"================================OK================================")

imgShiftHs(jpg_files)
imgShiftVs(jpg_files)
img_contrast(jpg_files)
imgFlip_left2right(jpg_files)
imgFlip_top2bottom(jpg_files)
img_brightness(jpg_files)

for img in set(glob.glob(img_path + "/*.bmp" or img_path + "/*.BMP")):
    img = img.replace("\\", "/")
    # print(f"file:{img}")

    shutil.move(img, bmp_path)


print(f"==============================BMP OK================================")

