#-*- encoding: utf-8 -*-
import os
from PIL import Image
import glob
import cv2
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import ImageFilter
from PIL import ImageEnhance
import sys
import random
from PIL import Image, ImageEnhance, ImageChops
print(sys.getdefaultencoding())
print(f"원하는 것을 선택하세요 ")
print(f"1.img좌우Shift  2.좌우반전 3.상하반전 4.ALL 5.imgRotate50 6.img상하Shift 7.gaussian 8.contrast 9.brightness ")
choice_option = str(input())
print(f"이미지 경로입력하세요(마지막 \를 제외)!")
img_path = str(input())
files = glob.glob(img_path + '/*.jpg' or '/*.bmp' or '/*.BMP' or '/*.JPG')

'''
#상하 이동
width, height = image.size
shift = random.randint(0, height * 0.2)
vertical_shift_image = ImageChops.offset(image, 0, shift)
vertical_shift_image.paste((0), (0, 0, width, shift))
vertical_shift_image.save('_vertical_shift.png')

'''

def imgShiftHs(files):

    print(f"|**************** aug_shift폴더에 저장됩니다.****************|")
    folder_name = str("aug_shiftHs")

    for idx, file in enumerate(files):

        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        image = image.convert('RGB')
        
        width, height = image.size
        base_name = os.path.basename(replace_path).split('.')[0]
        
        shift = random.randint(0, width*0.5)
        horizonal_shift_image = ImageChops.offset(image, shift, 0)
        horizonal_shift_image.paste((0), (0, 0, shift, height))
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        horizonal_shift_image.save(os.path.join(img_path,folder_name,f"{base_name}_Hs{idx}.jpg"))
    print(f"ok")


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
        
        shift = random.randint(0, height*0.5)
        vertical_shift_image = ImageChops.offset(image, shift, 0)
        vertical_shift_image.paste((0), (0, 0, width, shift))
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        vertical_shift_image.save(os.path.join(img_path,folder_name,f"{base_name}_Vh{idx}.jpg"))
    print(f"ok")
    
    
def imgRotate(files):

    print(f"|**************** aug_rt폴더에 저장됩니다.****************|")
    folder_name = str("aug_rt")
    print("원하는 각도 적으세요")
    rotate_num = float(input())
    num_range = round(360/ rotate_num)
    print(f"num range : {num_range}")


    for idx, file in enumerate(files):

        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        image = image.convert('RGB')
        base_name = os.path.basename(replace_path).split('.')[0]
        #print(base_name)

        for i in range(num_range):
            #rotate_image = image.rotate(i) #시계방향 35도 회전
            #print(f"rotate_image:{rotate_image}")
            rotate_image = image.rotate(rotate_num * i) #시계방향 35도 회전
            os.makedirs(os.path.join(img_path,folder_name), exist_ok=True)
            rotate_image.save(os.path.join(img_path,folder_name,f"{base_name}_R{i}.jpg"))
    print(f"ok")

def imgRotate35(files):

    print(f"|**************** aug_rt폴더에 저장됩니다.****************|")
    print(f"360도 기준")
    folder_name = str("aug_rt")
    #print("원하는 각도 적으세요")
    #rotate_num = float(input())
    #num_range = round((5 / rotate_num))
    #print(f"num range : {num_range}")


    for idx, file in enumerate(files):

        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        #print(base_name)

        for i in range(1,360,45):
            rotate_image = image.rotate(i) #시계방향 35도 회전
            print(f"rotate_image:{rotate_image}")
            #rotate_image = image.rotate(rotate_num * i) #시계방향 35도 회전
            os.makedirs(os.path.join(img_path,folder_name), exist_ok=True)
            rotate_image.save(os.path.join(img_path,folder_name,f"{base_name}_R{i}.jpg"))
    print(f"ok")


def imgFlip_left2right(files):
    print(f"|**************** aug_h_flip 폴더에 저장됩니다.****************|")
    folder_name = str("aug_Hflip")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        flip_image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(img_path,folder_name,f"{base_name}_Hf{idx}.jpg"))

def imgFlip_top2bottom(files):

    print(f"|**************** aug_v_flip 폴더에 저장됩니다.****************|")
    folder_name = str("aug_Vflip")

    for idx, file in enumerate(files):

        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]

        flip_image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(img_path,folder_name,f"{base_name}_Vf{idx}.jpg"))


def img_sharpen(files):


    print(f"|**************** aug_sharpen 폴더에 저장됩니다.****************|")
    folder_name = str("aug_sharpen")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]

        flip_image = image.filter(ImageFilter.SHARPEN)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_sharpen_{idx}.jpg"))


def img_contour(files):

    print(f"|**************** aug_contour 폴더에 저장됩니다.****************|")
    folder_name = str("aug_contour")


    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]

        flip_image = image.filter(ImageFilter.CONTOUR)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_contour_{idx}.jpg"))



def img_median(files):
    print(f"|**************** aug_median 폴더에 저장됩니다.****************|")
    folder_name = str("aug_median")

    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]


        flip_image = image.filter(ImageFilter.MedianFilter)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        flip_image.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_median_{idx}.jpg"))

def img_gaussian(files):
    print(f"|**************** aug_sharpen 폴더에 저장됩니다.****************|")
    folder_name = str("aug_gaussian")


    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        gaussian_image = image.filter(ImageFilter.GaussianBlur(1))
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        gaussian_image.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_gaussian_{idx}.jpg"))


def img_contrast(files):
    print(f"|**************** img_contrast 폴더에 저장됩니다.****************|")
    folder_name = str("aug_contrast")


    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        enhancer = ImageEnhance.Sharpness(image)
        enhancer = enhancer.enhance(1.8)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        enhancer.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_enhancer_{idx}.jpg"))

def img_brightness(files):
    print(f"|**************** img_contrast 폴더에 저장됩니다.****************|")
    folder_name = str("aug_brightness")


    for idx, file in enumerate(files):
        replace_path = file.replace("\\", "/")
        image = Image.open(replace_path)
        base_name = os.path.basename(replace_path).split('.')[0]
        enhancer = ImageEnhance.Brightness(image)
        enhancer = enhancer.enhance(1.5)
        os.makedirs(os.path.join(img_path, folder_name), exist_ok=True)
        enhancer.save(os.path.join(img_path,folder_name,f"{base_name}_Aug_brightness_{idx}.jpg"))


if choice_option == str(1):
    imgShiftHs(files)
    #imgRotate(files)

elif choice_option == str(2):
    imgFlip_left2right(files)

elif choice_option == str(3):
    imgFlip_top2bottom(files)

elif choice_option == str(4):
    imgShiftHs(files)
    imgFlip_left2right(files)
    imgFlip_top2bottom(files)
    imgShiftVs(files)
    img_brightness(files)
    

elif choice_option == str(5):
    imgRotate35(files)

elif choice_option == str(6):
    imgShiftVs(files)

elif choice_option == str(7):
    img_gaussian(files)

elif choice_option == str(8):
    img_contrast(files)


elif choice_option == str(9):
    img_brightness(files)













