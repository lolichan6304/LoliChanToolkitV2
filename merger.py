from PIL import Image
import numpy as np
import glob, os

# GLOBALS
#folder = "./House Maid/"
database = "./database"
compiled = "./local"
MAX = 40000

# build directory structure
print("Copying Directory Structure...")
for dirpath, dirnames, filenames in os.walk(database):
    structure = os.path.join(compiled, dirpath[len(database)+1:])
    if not os.path.isdir(structure):
        os.mkdir(structure)
        print("Made Folder {}".format(structure))
    else:
        print("Folder {} does already exits!".format(structure))

for folder in sorted(os.listdir(database)):
    for chapter in os.listdir(os.path.join(database,folder)):
        print("Working on folder: {}".format(chapter))
        # check directory in compiled
        list_pages = sorted(os.listdir(os.path.join(compiled, folder, chapter)))
        # Check if the chapter is merged in compiled
        if len(list_pages) > 0:
            print("Folder has been merged! Moving to next Folder")
        else:
            # counter for page number
            list_pages = sorted(list(filter(lambda x: "pic" in x, os.listdir(os.path.join(database, folder, chapter)))))
            print("Number of Pages: {}".format(len(list_pages)))
            page = 1
            img = None
            for i in list_pages:
                if img is None:
                    img = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                    if img.shape[1] != 720 and img.shape[1] != 900:
                        img = None
                else:
                    # load image first
                    temp = np.asarray(Image.open(os.path.join(database, folder, chapter, i)).convert("RGB"))
                    length = temp.shape[0]
                    if (img.shape[0] + temp.shape[0]) <= MAX:
                        if temp.shape[1] != 720 and temp.shape[1] != 900:
                            img = img
                        else:
                            #print(i, temp.shape)
                            img = np.concatenate([img, temp], 0)
                    else:
                        # here we hit max length
                        # save the current image
                        to_save = Image.fromarray(img).save(os.path.join(compiled, folder, chapter, "compic_{:03d}.png".format(page)))
                        page += 1
                        # reset length of image
                        if temp.shape[1] != 720 and temp.shape[1] != 900:
                            img = None
                        else:
                            img = temp
            to_save = Image.fromarray(img).save(os.path.join(compiled, folder, chapter, "compic_{:03d}.png".format(page)))
            print("Merge complete! Number of pages merged to: {}".format(page))
        



