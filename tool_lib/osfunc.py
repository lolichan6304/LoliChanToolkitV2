import os

def create_directory_structure(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("{} directory does not exist, folder created".format(folder))
    else:
        print("{} directory exists, no files are changed".format(folder))

def copy_directory_structure(fro="./database", to="./local"):
    print("copying directory dtructure...")
    for dirpath, dirnames, filenames in os.walk(fro):
        structure = os.path.join(to, dirpath[len(fro)+1:])
        if not os.path.isdir(structure):
            os.mkdir(structure)
            print("made folder {}".format(structure))
        else:
            print("folder {} already exists!".format(structure))