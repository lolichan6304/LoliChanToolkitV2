import os

def create_directory_structure(database="./database", compiled="./local"):
    if not os.path.exists(database):
        os.mkdir(database)
        print("{} directory does not exist, folder created".format(database))
    else:
        print("{} directory exists, no files are changed".format(database))
    if not os.path.exists(compiled):
        os.mkdir(compiled)
        print("{} directory does not exist, folder created".format(compiled))
    else:
        print("{} directory exists, no files are changed".format(compiled))

def copy_directory_structure(fro="./database", to="./local"):
    print("copying directory dtructure...")
    for dirpath, dirnames, filenames in os.walk(fro):
        structure = os.path.join(to, dirpath[len(fro)+1:])
        if not os.path.isdir(structure):
            os.mkdir(structure)
            print("made folder {}".format(structure))
        else:
            print("folder {} already exists!".format(structure))