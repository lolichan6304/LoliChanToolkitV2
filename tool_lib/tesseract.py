import pytesseract
from pytesseract import Output
import cv2
from PIL import Image
import numpy as np
import os

accepted_lang = ["kor", "chi_tra"]

def ocr(database, compiled, lang):
    for folder in sorted(os.listdir(database)):
        for chapter in os.listdir(os.path.join(database,folder)):
            print("working on folder: {}".format(chapter))
            # check directory in compiled
            list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
            # Check if the chapter is cropped in compiled
            if len(list_pages) > 0:
                print("folder has been cropped! moving to next folder")
            else:
                list_pages = sorted(os.listdir(os.path.join(database, folder, chapter)))
                print("number of pages: {}".format(len(list_pages)))
                for i in list_pages:
                    img = Image.open(os.path.join(database, folder, chapter, i)).convert('L')
                    img.save(os.path.join(compiled, folder, chapter, i), dpi=(300, 300))
                    img = cv2.imread(os.path.join(compiled, folder, chapter, i), 0)
                    d = pytesseract.image_to_data(img, lang=lang, config='--psm 11 --oem 3', output_type=Output.DICT)
                    text = pytesseract.image_to_string(img, lang=lang, config='--psm 11 --oem 3')
                    n_boxes = len(d['level'])
                    for j in range(n_boxes):
                        if d['level'][j] == 4:
                            (x, y, w, h) = (d['left'][j], d['top'][j], d['width'][j], d['height'][j])
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.imwrite(os.path.join(compiled, folder, chapter, i), img)
                    with open(os.path.join(compiled, folder, chapter, i[:-4]+".txt"), "w", 5, "utf-8") as text_file:
                        text_file.write(text)
                        text_file.close()


'''file_path = './database/Ex Wife/TOPTOON_頂通-國際官方中文版-韓國最新漫畫-線上免費看_-_與前妻同居_-_第1話/pic_0{}.jpg'
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
        text_file.close()'''