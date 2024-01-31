import cv2
import numpy as np
from math import floor
import math
from pathlib import Path
import os
import matplotlib.pyplot as plt
from PIL import Image
#print(os.listdir('../../Desktop/cat.png'))
img_path = '../../Desktop/cat.png'
#img_path = Path(img_path).absolute()
#print(f"절대경로 : {img_path}")

img = Image.open(img_path).convert('L')
img = np.array(img)

def img_scale(img_path, target_size):
    img = cv2.imread(img_path)
    print(f"shape : {img.shape}, dtype: {img.dtype}")
    height = img.shape[0]
    width = img.shape[1]

    target_size = (300, 300)  # target size
    output = np.zeros((target_size[0], target_size[1], 3), np.uint8)

    x_scale = height / output.shape[0]  # input image / output image
    y_scale = width / output.shape[1]  # input image / output image

    for y in range(output.shape[1]):
        for x in range(output.shape[0]):
            # the pixel at coordinate (x, y) in the new image is equal to the pixel that is located at coordinate (floor(x * x_ratio), floor(y * y_ratio)).
            # floor는 인접한 픽셀을 가져오기 위해서 사용
            xp, yp = floor(x * x_scale), floor(y * y_scale)
            #print(xp, yp)
            #print(x, y)
            output[x, y] = img[xp, yp]
    return cv2.imwrite( '../../Desktop/scale_cat.png', output)




roberts_1 = np.array([[ 1, 0],
                      [ 0,-1]])

roberts_2 = np.array([[ 0, 1],
                      [-1, 0]])

sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_y = np.array([[ 1, 2, 1],
                    [ 0, 0, 0],
                    [-1,-2,-1]])

prewitt_x = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])

prewitt_y = np.array([[ 1, 1, 1],
                      [ 0, 0, 0],
                      [-1,-1,-1]])

LoG_3_1 = np.array([[ 0,-1, 0],
                    [-1, 4,-1],
                    [ 0,-1, 0]])

LoG_3_2 = np.array([[-1,-1,-1],
                    [-1, 8,-1],
                    [-1,-1,-1]])

LoG_5 = np.array([[ 0, 0,-1, 0, 0],
                  [ 0,-1,-2,-1, 0],
                  [-1,-2,16,-2,-1],
                  [ 0,-1,-2,-1, 0],
                  [ 0, 0,-1, 0, 0]])

LoG_9 = np.array([[ 0, 1, 1,  2,  2,  2, 1, 1, 0],
                  [ 1, 2, 4,  5,  5,  5, 4, 2, 1],
                  [ 1, 4, 5,  3,  0,  3, 5, 4, 1],
                  [ 2, 5, 3,-12,-24,-12, 3, 5, 2],
                  [ 2, 5, 0,-24,-40,-24, 0, 5, 2],
                  [ 2, 5, 3,-12,-24,-12, 3, 5, 2],
                  [ 1, 4, 5,  3,  0,  3, 5, 4, 1],
                  [ 1, 2, 4,  5,  5,  5, 4, 2, 1],
                  [ 0, 1, 1,  2,  2,  2, 1, 1, 0]])



def show(img, result1,result2,result, thr_result):


    plt.subplot(2, 3, 1)
    plt.imshow(img,cmap='gray')
    plt.title("img")

    plt.subplot(2, 3, 2)
    plt.imshow(result1, cmap='gray')
    plt.title("result1")

    plt.subplot(2, 3, 3)
    plt.imshow(result2, cmap='gray')
    plt.title("result2")

    plt.subplot(2, 3, 4)
    plt.imshow(result, cmap='gray')
    plt.title("result")

    plt.subplot(2, 3, 5)
    plt.imshow(thr_result, cmap='gray')
    plt.title("thr_result")

    plt.tight_layout()
    plt.show()


def edge_detection(img, mask1, mask2, threshold, show_img=True):
    img_shape = img.shape

    try:
        if mask1.shape != mask2.shape:
            raise Exception('마스크의 크기가 서로 다릅니다.')
        filter_size = mask1.shape
    except Exception as e:
        print('예외가 발생했습니다.', e)

    result_shape = tuple(np.array(img_shape) - np.array(filter_size) + 1)

    result1 = np.zeros(result_shape)
    result2 = np.zeros(result_shape)

    for h in range(0, result_shape[0]):
        for w in range(0, result_shape[1]):
            tmp = img[h:h + filter_size[0], w:w + filter_size[1]]
            result1[h, w] = np.abs(np.sum(tmp * mask1))
            result2[h, w] = np.abs(np.sum(tmp * mask2))

    result = result1 + result2

    thr_result = np.zeros(result_shape)
    thr_result[result > threshold] = 1

    if show_img:
        show(img, result1, result2, result, thr_result)

    return result1, result2, result, thr_result


edge_detection(img, prewitt_x, prewitt_y, threshold=70)


def median_filter(img, filter_size=(3, 3), stride=1):
    img_shape = np.shape(img)

    result_shape = tuple(np.int64((np.array(img_shape) - np.array(filter_size)) / stride + 1))

    result = np.zeros(result_shape)

    for h in range(0, result_shape[0], stride):
        for w in range(0, result_shape[1], stride):
            tmp = img[h:h + filter_size[0], w:w + filter_size[1]]
            tmp = np.sort(tmp.ravel())
            result[h, w] = tmp[int(filter_size[0] * filter_size[1] / 2)]

    return result


def median_filter_show(img, max_ylim=12500):
    # show image
    plt.subplot(2,2,1)
    plt.imshow(img, cmap='gray')

    # show histogram
    if max_ylim != 'none':
        axes = plt.axes()
        axes.set_ylim([0, max_ylim])

    plt.subplot(2, 2, 2)
    plt.hist(img.ravel(), bins=256, range=[0, 256])

    plt.show()


med_img_1 = median_filter(img)
median_filter_show(med_img_1, max_ylim=12500)