#-*- coding: utf-8 -*-
import math
from math import radians, sin, cos
from PIL import Image
import glob,os, cv2
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

class augmentation:

    def __init__(self):

        #path = r"D:\AI_SVT_Training_mk\annotations\annos"
        print(f"PATH 경로 입력")

        path =str(input())
        self.path = path
        self.path = self.path.replace("\\","/")

        self.image = [i.replace("\\",'/') for i in (glob.glob(os.path.join(f"{self.path}/*"))) if i.endswith(("jpg","JPG"))]
        self.xml = [i.replace("\\",'/') for i in (glob.glob(os.path.join(f"{self.path}/*"))) if i.endswith(".xml")]


        self.abs_path = r"D:\AI_SVT_Training_mk\annotations\annos"



        self.SAVE_XSHIFT_IMG_path = os.path.join(self.path,"Xshift_image")
        self.SAVE_YSHIFT_IMG_path = os.path.join(self.path,"Yshift_image")
        self.SAVE_Hfilp_IMG_path = os.path.join(self.path,"Hfilp_image")
        self.SAVE_Vfilp_IMG_path = os.path.join(self.path,"Vfilp_image")
        self.SAVE_Rotate_IMG_path = os.path.join(self.path,"Rotate_image")





        self.shift_X = [1,2,3,5,10,15,20,40,50,70,100]
        self.shift_X.sort()
        self.shift_Y = [5, 50, 100, -5, -50, -100]
        self.shift_Y.sort()
        self.want_angle = 45
        self.rotate_angle=[*range(5,355,self.want_angle)]
        #print(f"self.rotate_angle:{self.rotate_angle}")




    def warning(self):
        if len(self.image) != len(self.xml):
            print(f"=========================")
            print(f"xml, jpg 파일 갯수 안맞음 !")
            print(f"다시확인!")
            print(f"=========================")

        else:
            pass


    def rotateIMG(self):
        self.warning()
        os.makedirs(self.SAVE_Rotate_IMG_path, exist_ok=True)

        for i in self.image:
            img_name = os.path.basename(i)
            img_name = img_name.split('.')[0]

            img = cv2.imread(i)
            h, w = img.shape[:2]
            cX, cY = w // 2, h // 2
            # 이미지의 중심을 중심으로 이미지를 45도 회전합니다.
            for idx in range(len(self.rotate_angle)):
                M = cv2.getRotationMatrix2D((cX, cY), self.rotate_angle[idx], 1.0)
                rotated_img = cv2.warpAffine(img, M, (w, h))

                cv2.imwrite(os.path.join(self.SAVE_Rotate_IMG_path,f"{img_name}_R{idx}.jpg"),rotated_img)



    def rotateXML(self):


        for idx in range(len(self.rotate_angle)):

            for i in self.xml:

                targetXML = open(i , 'rt', encoding='UTF8')
                tree = ET.parse(targetXML)
                root = tree.getroot()

                for size in root.iter('size'):
                    width = size.find('width').text
                    self.width = eval(width)
                    height = size.find('height').text
                    self.height = eval(height)

                    self.cx =self.width //2
                    self.cy =self.height //2


                for obj in root.iter('object'):
                    xmin = (obj.find('bndbox')[0]).text
                    xmin = eval(xmin)
                    ymin = obj.find('bndbox')[1].text
                    ymin = eval(ymin)
                    xmax = obj.find('bndbox')[2].text
                    xmax = eval(xmax)
                    ymax = obj.find('bndbox')[3].text
                    ymax = eval(ymax)

                    P1_x, P1_y = self.Ccalc_rotate(xmin, ymin, self.cx, self.cy, theta=self.rotate_angle[idx])
                    P2_x, P2_y = self.Ccalc_rotate(xmax, ymin, self.cx, self.cy, theta=self.rotate_angle[idx])
                    P3_x, P3_y = self.Ccalc_rotate(xmin, ymax, self.cx, self.cy, theta=self.rotate_angle[idx])
                    P4_x, P4_y = self.Ccalc_rotate(xmax, ymax, self.cx, self.cy, theta=self.rotate_angle[idx])


                    gap_xmin = abs(P1_x-P2_x)

                    min_xmin = min(P1_x,P2_x,P3_x,P4_x)
                    min_ymin = min(P1_y, P2_y, P3_y, P4_y)
                    max_xmax = max (P1_x,P2_x,P3_x,P4_x)
                    max_ymax = max(P1_y,P2_y,P3_y,P4_y)

                    '''


                    if P1_x > P3_x :

                        P3_x = P1_x
                        P3_y = P1_y
                        P4_x = P2_x
                        P4_y = P2_y




                    if P1_x < P2_x :
                        new_xmin = P2_x-gap_x
                    elif P1_x > P2_x :
                        new_xmin = P1_x-gap_x

                    if P1_y < P2_y :
                        new_ymin = P1_y
                    elif P1_y < P2_y :
                        new_ymin = P2_y'''

                    if min_xmin > max_xmax:
                        obj.find('bndbox')[0].text = str(max_xmax)
                        obj.find('bndbox')[1].text = str(min_ymin)
                        obj.find('bndbox')[2].text = str(min_xmin)
                        obj.find('bndbox')[3].text = str(max_ymax)

                    else:


                        obj.find('bndbox')[0].text = str(min_xmin)
                        obj.find('bndbox')[1].text = str(min_ymin)
                        obj.find('bndbox')[2].text = str(max_xmax)
                        obj.find('bndbox')[3].text = str(max_ymax)











                    #cross_CX, cross_CY = self.get_crosspt(P1_x, P1_y, P4_x, P4_y, P2_x, P2_y, P3_x, P3_y)
                    #print(f"원래 cp = {self.cx},{self.cy}")

                    #print(f"새로운 cp point = {cross_CX},{cross_CY}")


                    #역행렬부분은 보류
                    '''

                    T_P1_x, T_P1_y = self.T_calc_rotate(P1_x, P1_y, cross_CX, cross_CY, self.height,self.width,theta=self.rotate_angle[idx])
                    #T_P2_x, T_P2_y = self.T_calc_rotate(P2_x, P2_y, cross_CX, cross_CY, self.height,self.width,theta=self.rotate_angle[idx])
                    #T_P3_x, T_P3_y = self.T_calc_rotate(P3_x, P3_y, cross_CX, cross_CY, self.height,self.width,theta=self.rotate_angle[idx])
                    T_P4_x, T_P4_y = self.T_calc_rotate(P4_x, P4_y, cross_CX, cross_CY, self.height,self.width,theta=self.rotate_angle[idx])

                    print(f"T_P1_x:{T_P1_x},T_P1_y:{T_P1_y},T_P4_x:{T_P4_x},T_P4_y:{T_P4_y}")
                    '''

                    '''
                    



                    obj.find('bndbox')[0].text = str(T_P1_x)
                    obj.find('bndbox')[1].text = str(T_P1_y)
                    obj.find('bndbox')[2].text = str(T_P4_x)
                    obj.find('bndbox')[3].text = str(T_P4_y)
                    '''



                # 파일이름변경
                target_tag_filename = root.find("filename")
                original = target_tag_filename.text  # 원본 String
                original_name = original.split(".")[0]

                modi_fileName = f"{original_name}_R{idx}.jpg"
                # print(f"modi_fileName:{modi_fileName}")
                modified_name = original.replace(original, modi_fileName)
                # print(f"modified_name:{modified_name}")
                target_tag_filename.text = modified_name

                # 파일path변경

                target_tag_path = root.find("path")
                # print(f"target_tag_path:{target_tag_path.text}")
                origin_path = target_tag_path.text

                modi_path = os.path.join(self.abs_path, f"{modi_fileName}")
                modi_path = modi_path.replace("/", "\\")
                print(f"modi_path:{modi_path}")

                modified = origin_path.replace(origin_path, modi_path)
                print(f"Rotate modified:{modified}")
                target_tag_path.text = modified

                tree.write(os.path.join(self.SAVE_Rotate_IMG_path, f"{modi_fileName.split('.')[0]}.xml"))

    def find_line_equation(self, x1, y1, x2, y2):
        # 기울기 계산
        m = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')

        # y 절편 계산
        b = y1 - m * x1 if m != float('inf') else None

        return m, b
    def Ccalc_rotate(self, x, y, img_cx, img_cy, theta=45):

        new_x = (x - img_cx) * cos(radians(360 - theta)) - (y - img_cy) * sin(radians(360 - theta)) + img_cx
        new_y = (x - img_cx) * sin(radians(360 - theta)) + (y - img_cy) * cos(radians(360 - theta)) + img_cy


        return int(new_x), int(new_y)




    def T_calc_rotate(self, x, y, img_cx, img_cy, height,width,theta=45):


        theta = -(theta)
        new_x = (x - img_cx) * cos(radians(360 - theta)) - (y - img_cy) * sin(radians(360 - theta)) + img_cx
        #new_x = (x - img_cx) * cos(radians(360 - theta)) - (y - img_cy) * sin(radians(360 - theta)) + img_cx
        #new_y = (x - img_cx) * sin(radians(360 - theta)) + (y - img_cy) * cos(radians(360 - theta)) + img_cy
        new_y = (x - img_cx) * sin(radians(360 - theta)) + (y - img_cy) * cos(radians(360 - theta)) + img_cy
        if new_y < 0:
            new_y = 0
        elif new_y > self.height:
            new_y = self.height
        elif new_x > self.width:
            new_x = self.width
        elif new_x < 0:
            new_x = 0
        return int(new_x), int(new_y)

    def get_crosspt(self, L1_START_X, L1_START_Y, L2_START_X, L2_START_Y, L3_START_X, L3_START_Y, L4_START_X, L4_START_Y):
        if L2_START_X == L1_START_X or L4_START_X == L3_START_X:
            print('delta x=0')
            if L2_START_X == L1_START_X:
                cx = L2_START_X
                m2 = (L4_START_Y - L3_START_Y) / (L4_START_X - L3_START_X)
                cy = m2 * (cx - L3_START_X) + L3_START_Y
                return cx, cy
            if L4_START_X == L3_START_X:
                cx = L4_START_X
                m1 = (L2_START_Y - L1_START_Y) / (L2_START_X - L1_START_X)
                cy = m1 * (cx - L1_START_X) + L1_START_Y
                return cx, cy

        m1 = (L2_START_Y - L1_START_Y) / (L2_START_X - L1_START_X)
        m2 = (L4_START_Y - L3_START_Y) / (L4_START_X - L3_START_X)

        if m1 == m2:
            print('parallel')
            return None


        cx = (L1_START_X * m1 - L1_START_Y - L3_START_X * m2 + L3_START_Y) / (m1 - m2)
        cy = m1 * (cx - L1_START_X) + L1_START_Y


        return int(cx), int(cy)




    def Xshift_img(self):
        self.warning()
        os.makedirs(self.SAVE_XSHIFT_IMG_path, exist_ok=True)

        for img in self.image:

            img_name = os.path.basename(img).split(".")[0]
            image = cv2.imread(img)
            height, width = image.shape[:2]

            for i in self.shift_X:

                x_shift = i
                y_shift = 0

                # 이동 행렬을 생성합니다.
                M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
                #print(F"m:{M}")

                shifted_image = cv2.warpAffine(image, M, (width, height))
                cv2.imwrite(os.path.join(self.SAVE_XSHIFT_IMG_path,f"{img_name}_XS{i}.jpg"),shifted_image)

    def Xshitf_xml(self):

        for i in self.shift_X:

            for xml in self.xml:
                self.xml_name = os.path.basename(xml).split(".")[0]


                targetXML = open(xml, 'rt', encoding='UTF8')
                tree = ET.parse(targetXML)
                root = tree.getroot()

                for size in root.iter('size'):
                    width = size.find('width').text
                    self.width = eval(width)



                for obj in root.iter('object'):
                    self.xmin = (obj.find('bndbox')[0]).text
                    self.xmin = eval(self.xmin)
                    self.ymin = obj.find('bndbox')[1].text
                    self.ymin = eval(self.ymin)
                    self.xmax = obj.find('bndbox')[2].text
                    self.xmax = eval(self.xmax)
                    self.ymax = obj.find('bndbox')[3].text
                    self.ymax = eval(self.ymax)



                    if self.xmin + i < 0:
                        obj.find('bndbox')[0].text = 0

                    elif self.xmin + i > self.width:
                        obj.find('bndbox')[0].text = self.width

                    obj.find('bndbox')[0].text = str(self.xmin + i)



                    if self.xmax + i < 0 :
                        obj.find('bndbox')[2].text = 0

                    elif self.xmax + i >self.width:
                        obj.find('bndbox')[2].text =self.width
                    obj.find('bndbox')[2].text = str(self.xmax + i)

                    #print(f"xmin:{self.xmin},ymin:{self.ymin},xmax:{self.xmax},ymax:{self.ymax}")

                #print(f"self.xmin:{self.xmin},self.xmax:{self.xmax}")

                #파일이름변경
                target_tag_filename =root.find("filename")
                original = target_tag_filename.text  # 원본 String
                original_name = original.split(".")[0]

                modi_fileName = f"{original_name}_XS{i}.jpg"
                #print(f"modi_fileName:{modi_fileName}")
                modified_name = original.replace(original, modi_fileName)
                #print(f"modified_name:{modified_name}")
                target_tag_filename.text = modified_name

                # 파일path변경

                target_tag_path = root.find("path")
                #print(f"target_tag_path:{target_tag_path.text}")
                origin_path = target_tag_path.text

                modi_path = os.path.join(self.abs_path,f"{modi_fileName}")
                modi_path = modi_path.replace("/","\\")


                modified = origin_path.replace(origin_path, modi_path)
                print(f"Xshift modified : {modified}")
                target_tag_path.text = modified

                tree.write(os.path.join(self.SAVE_XSHIFT_IMG_path, f"{modi_fileName.split('.')[0]}.xml"))


    def Yshift_img(self):
        self.warning()
        os.makedirs(self.SAVE_YSHIFT_IMG_path, exist_ok=True)

        for img in self.image:

            img_name = os.path.basename(img).split(".")[0]
            image = cv2.imread(img)
            height, width = image.shape[:2]

            for i in self.shift_Y:
                #print(f"i:{i}")
                x_shift = 0
                y_shift = i

                # 이동 행렬을 생성합니다.
                M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
                #print(F"m:{M}")

                shifted_image = cv2.warpAffine(image, M, (width, height))
                cv2.imwrite(os.path.join(self.SAVE_YSHIFT_IMG_path,f"{img_name}_YS{i}.jpg"),shifted_image)

    def Yshift_xml(self):

        for i in self.shift_Y:

            for xml in self.xml:
                self.xml_name = os.path.basename(xml).split(".")[0]
                targetXML = open(xml, 'rt', encoding='UTF8')
                tree = ET.parse(targetXML)
                root = tree.getroot()


                for size in root.iter('size'):
                    width = size.find('width').text
                    self.width = eval(width)
                    height = size.find('height').text
                    self.height = eval(height)


                for obj in root.iter('object'):
                    self.xmin = (obj.find('bndbox')[0]).text
                    self.xmin = eval(self.xmin)
                    self.ymin = obj.find('bndbox')[1].text
                    self.ymin = eval(self.ymin)
                    self.xmax = obj.find('bndbox')[2].text
                    self.xmax = eval(self.xmax)
                    self.ymax = obj.find('bndbox')[3].text
                    self.ymax = eval(self.ymax)



                    if self.ymin + i <0 :
                        obj.find('bndbox')[1].text = 0
                    elif self.ymin + i > self.height:
                        obj.find('bndbox')[1].text =self.height

                    obj.find('bndbox')[1].text = str(self.ymin + i)



                    if self.ymax + i < 0 :
                        obj.find('bndbox')[3].text = 0
                    elif self.ymax + i > self.height:
                        obj.find('bndbox')[3].text = self.height

                    obj.find('bndbox')[3].text = str(self.ymax + i)



                #파일이름변경
                target_tag_filename = root.find("filename")
                original = target_tag_filename.text  # 원본 String
                original_name = original.split(".")[0]

                modi_fileName = f"{original_name}_YS{i}.jpg"
                #print(f"modi_fileName:{modi_fileName}")
                modified_name = original.replace(original, modi_fileName)
                #print(f"modified_name:{modified_name}")
                target_tag_filename.text = modified_name

                # 파일path변경

                target_tag_path =root.find("path")
                #print(f"target_tag_path:{target_tag_path.text}")
                origin_path = target_tag_path.text

                modi_path = os.path.join(self.abs_path,f"{modi_fileName}")
                modi_path = modi_path.replace("/","\\")


                modified = origin_path.replace(origin_path, modi_path)
                print(f"Yshift modified : {modified}")
                target_tag_path.text = modified

                tree.write(os.path.join(self.SAVE_YSHIFT_IMG_path, f"{modi_fileName.split('.')[0]}.xml"))

    def Hfilp_IMG(self):
        os.makedirs(self.SAVE_Hfilp_IMG_path, exist_ok=True)

        for img in self.image:

            img_name = os.path.basename(img).split(".")[0]
            image = cv2.imread(img)
            H_img = cv2.flip(image,1 )#수평으로 뒤집기
            cv2.imwrite(os.path.join(self.SAVE_Hfilp_IMG_path,f"{img_name}_H.jpg"),H_img)

    def Hfilp_xml(self):

        for xml in self.xml:

            targetXML = open(xml, 'rt', encoding='UTF8')
            tree = ET.parse(targetXML)
            root = tree.getroot()

            for size in root.iter('size'):
                width = size.find('width').text
                self.width = eval(width)

            for obj in root.iter('object'):
                self.xmin = (obj.find('bndbox')[0]).text
                self.xmin = eval(self.xmin)
                self.new_xmin = (self.width - self.xmin -1)

                self.xmax = obj.find('bndbox')[2].text
                self.xmax = eval(self.xmax)
                self.new_xmax = (self.width - self.xmax -1)




                if self.new_xmin < 0:
                    obj.find('bndbox')[0].text = 0
                elif self.new_xmin > self.width:
                    obj.find('bndbox')[0].text = str(self.width)

                obj.find('bndbox')[0].text = str(self.new_xmin)




                if self.xmax < 0:
                    obj.find('bndbox')[2].text = 0
                elif self.xmax > self.width:
                    obj.find('bndbox')[2].text = str(self.width)
                obj.find('bndbox')[2].text = str(self.new_xmax)





            # 파일이름변경
            target_tag_filename = root.find("filename")
            original = target_tag_filename.text  # 원본 String
            original_name = original.split(".")[0]
            #print(f"original_name:{original_name}")

            modi_fileName = f"{original_name}_H.jpg"
            #print(f"modi_fileName:{modi_fileName}")
            modified_name = original.replace(original, modi_fileName)
            #print(f"modified_name:{modified_name}")
            target_tag_filename.text = modified_name
            #print(f"target_tag_filename.text:{target_tag_filename.text}")




            # 파일path변경

            target_tag_path = root.find("path")
            # print(f"target_tag_path:{target_tag_path.text}")
            origin_path = target_tag_path.text

            modi_path = os.path.join(self.abs_path, f"{modi_fileName}")
            #modi_path = modi_path.replace("/","\\")


            modified = origin_path.replace(origin_path, modi_path)
            print(f"Hfilp modified = {modified}")
            target_tag_path.text = modified

            tree.write(os.path.join(self.SAVE_Hfilp_IMG_path, f"{modi_fileName.split('.')[0]}.xml"))







    def Vfilp_IMG(self):
        os.makedirs(self.SAVE_Vfilp_IMG_path, exist_ok=True)

        for img in self.image:
            img_name = os.path.basename(img).split(".")[0]
            image = cv2.imread(img)
            H_img = cv2.flip(image, 0)#상하반전
            cv2.imwrite(os.path.join(self.SAVE_Vfilp_IMG_path, f"{img_name}_V.jpg"), H_img)


    def Vfilp_xml(self):
        for xml in self.xml:
            self.xml_name = os.path.basename(xml).split(".")[0]


            targetXML = open(xml, 'rt', encoding='UTF8')
            tree = ET.parse(targetXML)
            root = tree.getroot()

            for size in root.iter('size'):
                height = size.find('height').text
                self.height = eval(height)

            for obj in root.iter('object'):
                self.ymin = (obj.find('bndbox')[1]).text
                self.ymin = eval(self.ymin)
                self.new_ymin = (self.height - self.ymin -1)

                self.ymax = obj.find('bndbox')[3].text
                self.ymax = eval(self.ymax)
                self.new_ymax = (self.height - self.ymax -1)


                if self.new_ymin < 0:
                    obj.find('bndbox')[1].text = 0
                elif self.new_ymin > self.height:
                    obj.find('bndbox')[1].text = str(self.height)

                obj.find('bndbox')[1].text = str(self.new_ymin)



                if self.new_ymax < 0:
                    obj.find('bndbox')[3].text = 0
                elif self.new_ymax > self.height:
                    obj.find('bndbox')[3].text = str(self.height)

                obj.find('bndbox')[3].text = str(self.new_ymax)

            # 파일이름변경
            target_tag_filename = root.find("filename")
            original = target_tag_filename.text  # 원본 String
            original_name = original.split(".")[0]

            modi_fileName = f"{original_name}_V.jpg"
            # print(f"modi_fileName:{modi_fileName}")
            modified_name = original.replace(original, modi_fileName)
            # print(f"modified_name:{modified_name}")
            target_tag_filename.text = modified_name

            # 파일path변경

            target_tag_path = root.find("path")
            # print(f"target_tag_path:{target_tag_path.text}")
            origin_path = target_tag_path.text

            modi_path = os.path.join(self.abs_path, f"{modi_fileName}")
            modi_path = modi_path.replace("/","\\")

            modified = origin_path.replace(origin_path, modi_path)
            print(f"Vfilp modified : {modified}")
            target_tag_path.text = modified

            tree.write(os.path.join(self.SAVE_Vfilp_IMG_path, f"{modi_fileName.split('.')[0]}.xml"))


if __name__ == "__main__":








    #augmentation().Vfilp_IMG()
    #augmentation().Vfilp_xml()
    #augmentation().Hfilp_IMG()
    #augmentation().Hfilp_xml()


    augmentation().rotateIMG()
    augmentation().rotateXML()


    #augmentation().Yshift_img()
    #augmentation().Yshift_xml()
    #augmentation().Xshift_img()
    #augmentation().Xshitf_xml()















