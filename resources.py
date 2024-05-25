import re
import plistlib
import os
import sys
import shutil
import traceback
import time
from PIL import Image
from os.path import join, isfile, isdir, splitext, abspath

def convert(dir, resources_dir, files, suffix):
    pass

def main():
    try:
        pack = abspath(input("Enter your 2.1 pack path: "))
        files_list = [f for f in os.listdir(pack) if isfile(join(pack, f))]
    except:
        print("Wrong/Invalid pack path!")
        print(traceback.format_exc())
        print()
        main()

    try:
        resources = abspath(input("Enter your GD Resources folder path: "))
        resources_files_list = [f for f in os.listdir(resources) if isfile(join(resources, f))]
    except:
        print("Wrong/Invalid resources path!")
        print(traceback.format_exc())
        print()
        main()

    try:
        os.mkdir(join(pack, "output"))
    except:
        pass

    convertible = []

    for f in resources_files_list:
        if splitext(f)[0].endswith("-uhd") and f.endswith(".plist"):
            convertible.append(f)

    for f in resources_files_list:
        if splitext(f)[0] in convertible:
            convertible.append(f)
    
    for f in resources_files_list:
        if (splitext(f)[0] + "-uhd.plist") in convertible:
            convertible.append(f)

    for f in resources_files_list:
        if (splitext(f)[0][:-3] + ".plist") in convertible:
            convertible.append(f)
        
    convertible = [c for c in convertible if not c.startswith("PlayerExplosion")]
    convertible.sort()

    for f in files_list:
        if f not in convertible:
           shutil.copy(join(pack, f), join(pack, "output")) 

    tp_file_list = [f for f in files_list if f in convertible]

    files_low = []
    files_medium = []
    files_high = []

    for f in tp_file_list:
        if splitext(f)[0].endswith("-hd"):
            files_medium.append(f)
        elif splitext(f)[0].endswith("-uhd"):
            files_high.append(f)
        else:
            files_low.append(f) 

    input("Press enter to exit.")

if __name__ == "__main__":
    main()
