import cv2
import numpy as np


def fixColor(image):
    return (cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))


def filters(image, x, y):
    kernel = np.ones((3, 3), np.uint8)
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    gaussian = cv2.GaussianBlur(opening, (3, 3), 0)
    sharp = cv2.filter2D(gaussian, -1, filter)
    edges_canny = cv2.Canny(sharp, x, y)
    dilation_opening = cv2.dilate(edges_canny, kernel, iterations=1)
    return dilation_opening


def create_template(image):
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return cv2.Canny(opening, 50, 75)


def create_conturs(image, result, str):
    (cnts, _) = cv2.findContours(result.copy(), str, cv2.CHAIN_APPROX_NONE)
    black = np.zeros(shape=image.shape)
    for cnt in cnts:
        cv2.drawContours(black, cnt, -1, (255, 0, 0), 2)
    black = cv2.resize(black, (400, 400))
    cv2.imshow('black ', (black))
    return cnts


def create_bounding(image, cnt_templates, cnts, size, min_size, thershold, color):
    counter = 0
    for cnt in cnts:
        num = cv2.matchShapes(cnt, cnt_templates, cv2.CONTOURS_MATCH_I1, 0)
        area = cv2.contourArea(cnt)
        if (num < thershold and area > size and area < min_size):
            print(area, num)
            counter += 1
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    image = cv2.resize(image, (400, 400))
    print(counter)
    return image


def find_max(cnts, image):
    max = 0
    temp_cnt = None
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if max < w * h:
            max = w * h
            temp_cnt = cnt
    black = np.zeros(shape=image.shape)
    cv2.drawContours(black, temp_cnt, -1, (255, 0, 0), 2)
    black = cv2.resize(black, (400, 400))
    return temp_cnt


original_image = cv2.imread(r"Image-Processing-Python-Object-Detection-main/Images/Object Detection Template 01.jpeg ", 0)

original_image = cv2.resize(original_image, (400, 400))
template_mouse = cv2.imread(r"Image-Processing-Python-Object-Detection-main/Images/mouseTemplate.jpeg", 0)
template_coin = cv2.imread(r"Image-Processing-Python-Object-Detection-main/Images/coinTemplate.jpeg", 0)
cv2.imshow('first img', original_image)

# key_template=cv2.resize(key_template, (400, 400))

filtterd_mouse = create_template(template_mouse)
filtterd_coins = create_template(template_coin)
kernel = np.ones((3, 3), np.uint8)
filtterd_mouse = cv2.dilate(filtterd_mouse, kernel, None, None, iterations=2)
filtterd_coins = cv2.dilate(filtterd_coins, kernel, None, None, iterations=2)

mouse_contur = create_conturs(template_mouse, filtterd_mouse, cv2.RETR_EXTERNAL)
coin_contur = create_conturs(template_coin, filtterd_coins, cv2.RETR_EXTERNAL)

final_original_mouse = filters(original_image, 125, 600)
final_original_coins = filters(original_image, 200, 900)

cnts_mouse = create_conturs(original_image, final_original_mouse, cv2.RETR_EXTERNAL)
cnts_coins = create_conturs(original_image, final_original_coins, cv2.RETR_EXTERNAL)

max_contur_mouse = find_max(mouse_contur, template_mouse)
max_contur_coins = find_max(coin_contur, template_coin)
original_image = fixColor(original_image)
final_img = create_bounding(original_image, max_contur_mouse, cnts_mouse, 2200, 15000, 0.3, (255, 0, 0))
cv2.imshow('mouses_bound', final_img)
final_img = create_bounding(final_img, max_contur_coins, cnts_coins, 300, 1000, 0.5, (0, 255, 0))
cv2.imshow('final_img', final_img)
cv2.waitKey(0)

