import pytesseract
from pytesseract import Output
import cv2
from PIL import Image
import numpy as np

file_path = './database/Ex Wife/TOPTOON_頂通-國際官方中文版-韓國最新漫畫-線上免費看_-_與前妻同居_-_第1話/pic_0{}.jpg'
for j in range(10, 32):
    im = Image.open(file_path.format(j)).convert('RGB')
    im.save('ocr.png', dpi=(300, 300))
    image = cv2.imread('ocr.png')
    d = pytesseract.image_to_data(image, lang="chi_tra", output_type=Output.DICT)
    print(d)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if d['level'][i] == 4:
            print(d['text'][i])
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite("output_{}.png".format(j), image)
    """cv2.imshow('img', image)
    cv2.waitKey(0)"""
    image = cv2.imread('ocr.png')
    text = pytesseract.image_to_string(image, lang="chi_tra")
    with open("output_{}.txt".format(j), "w", 5, "utf-8") as text_file:
        text_file.write(text)
        text_file.close()