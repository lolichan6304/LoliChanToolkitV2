import os
import numpy as np
from PIL import Image

accepted_width = [688, 720, 900, 1000]

def merge_tool(database, compiled, MAX = 40000):
    # sanity check
    MAX = int(MAX)

    for folder in sorted(os.listdir(database)):
        if folder[-4:] != "json":
            for chapter in os.listdir(os.path.join(database,folder)):
                print("working on folder: {}".format(chapter))
                # check directory in compiled
                list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
                # Check if the chapter is merged in compiled
                if len(list_pages) > 0:
                    print("folder has been merged! moving to next Folder")
                else:
                    # counter for page number
                    #list_pages = sorted(list(filter(lambda x: "pic" in x, os.listdir(os.path.join(database, folder, chapter)))))
                    list_pages = sorted(os.listdir(os.path.join(database, folder, chapter)))
                    print("number of pages: {}".format(len(list_pages)))
                    page = 1
                    img = None
                    for i in list_pages:
                        if img is None:
                            img = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                            if img.shape[1] not in accepted_width:
                                img = None
                        else:
                            # load image first
                            temp = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                            length = temp.shape[0]
                            if (img.shape[0] + temp.shape[0]) <= MAX:
                                if temp.shape[1] not in accepted_width:
                                    img = img
                                else:
                                    #print(i, temp.shape)
                                    img = np.concatenate([img, temp], 0)
                            else:
                                # here we hit max length
                                # save the current image
                                to_save = Image.fromarray(img).save(os.path.join(compiled, folder, chapter, "compic_{:03d}.jpg".format(page)))
                                page += 1
                                # reset length of image
                                if temp.shape[1] not in accepted_width:
                                    img = None
                                else:
                                    img = temp
                    if img is not None:
                        to_save = Image.fromarray(img).save(os.path.join(compiled, folder, chapter, "compic_{:03d}.jpg".format(page)))
                    print("merge complete! number of pages merged to: {}".format(page))

def split_tool(database, compiled, MAX = 10000):
    # sanity check
    MAX = int(MAX)

    for folder in sorted(os.listdir(database)):
        for chapter in os.listdir(os.path.join(database,folder)):
            print("working on folder: {}".format(chapter))
            # check directory in compiled
            list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
            # Check if the chapter is merged in compiled
            if len(list_pages) > 0:
                print("folder has been split! moving to next Folder")
            else:
                # counter for page number
                list_pages = sorted(os.listdir(os.path.join(database, folder, chapter)))
                print("number of pages: {}".format(len(list_pages)))
                page = 1
                for i in list_pages:
                    img = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                    curr = 0
                    while img.shape[0] - curr*MAX > MAX: # this is the last one
                        to_save = Image.fromarray(img[curr*MAX:(curr+1)*MAX,:]).save(os.path.join(compiled, folder, chapter, "splpic_{:03d}.jpg".format(page)))
                        curr += 1
                        page += 1
                    to_save = Image.fromarray(img[curr*MAX:,:]).save(os.path.join(compiled, folder, chapter, "splpic_{:03d}.jpg".format(page)))
                    page += 1
                print("split complete! number of pages split to: {}".format(page))

def crop_tool(database, compiled, WIDTH = 720, reverse=True, MAX=20000):
    # sanity check
    assert WIDTH in accepted_width, "WIDTH provided {} is not accepted! suggested value: 720"

    for folder in sorted(os.listdir(database)):
        for chapter in os.listdir(os.path.join(database,folder)):
            print("working on folder: {}".format(chapter))
            # check directory in compiled
            list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
            # Check if the chapter is cropped in compiled
            if len(list_pages) > 0:
                print("folder has been cropped! moving to next folder")
            else:
                # counter for page number
                list_pages = sorted(os.listdir(os.path.join(database, folder, chapter)), reverse=reverse)
                print("number of pages: {}".format(len(list_pages)))
                page = 1
                for i in list_pages:
                    img = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                    # get region
                    assert img.shape[1]%2 == WIDTH%2, "WIDTH and image shape should have same odd/even values, got {}, {} instead".format(img.shape[0], WIDTH)
                    region = img[:,(img.shape[1]-WIDTH)//2:(img.shape[1]-WIDTH)//2+WIDTH,:]
                    to_save = Image.fromarray(region).save(os.path.join(compiled, folder, chapter, "pic_{:03d}.jpg".format(page)))
                    #to_save = Image.fromarray(region).save(os.path.join(compiled, folder, chapter, i.split(".")[0]+".jpg"))
                    page += 1
                print("crop complete! number of pages cropped to: {}".format(page-1))

                # counter for page number
                list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
                print("number of pages: {}".format(len(list_pages)))
                page = 1
                for i in list_pages:
                    img = np.asarray(Image.open(os.path.join(compiled, folder, chapter, i)).convert("RGB"))
                    curr = 0
                    while img.shape[0] - curr*MAX > MAX: # this is the last one
                        to_save = Image.fromarray(img[curr*MAX:(curr+1)*MAX,:]).save(os.path.join(compiled, folder, chapter, "finpic_{:03d}.jpg".format(page)))
                        #to_save = Image.fromarray(img[curr*MAX:(curr+1)*MAX,:]).save(os.path.join(compiled, folder, chapter, i.split(".")[0]+"_{:03d}.jpg".format(page)))
                        curr += 1
                        page += 1
                    to_save = Image.fromarray(img[curr*MAX:,:]).save(os.path.join(compiled, folder, chapter, "finpic_{:03d}.jpg".format(page)))
                    #to_save = Image.fromarray(img[curr*MAX:,:]).save(os.path.join(compiled, folder, chapter, i.split(".")[0]+"_{:03d}.jpg".format(page)))
                    page += 1
                print("split complete! number of pages split to: {}".format(page))