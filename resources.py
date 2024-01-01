import re
import plistlib
import os, sys, shutil
import traceback
import time
from PIL import Image
from os.path import join, isfile, isdir, splitext, abspath

def convert(dir, resources_dir, files, suffix):
    # oh boy here we go again
    pass

def main():
    try:
        pack = abspath(input("Enter your 2.1 pack path: "))
        files_list = [f for f in os.listdir(pack) if isfile(join(pack, f))]
    except:
        # If the input is incorrect,
        # prints the error message and ask for input again
        print("Wrong/Invalid pack path!")
        print(traceback.format_exc())
        print()
        main()
        return "balls"

    try:
        # resources = abspath(input("Enter your 2.2 resources folder path: "))
        resources = "D:\Steam\steamapps\common\Geometry Dash\Resources"
        resources_files_list = [f for f in os.listdir(resources) if isfile(join(resources, f))]
    except:
        print("Wrong/Invalid resources path!")
        print(traceback.format_exc())
        print()
        main()
        return "balls"

    try:
        os.mkdir(join(pack, "output"))
    except:
        pass

    convertible = []

    # im too lazy to optimize this for now
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

    ACTUAL_files_list = [f for f in files_list if f in convertible]

    files_low = []
    files_medium = []
    files_high = []

    # Separating between graphic types
    for f in ACTUAL_files_list:
        if splitext(f)[0].endswith("-hd"):
            files_medium.append(f)
        elif splitext(f)[0].endswith("-uhd"):
            files_high.append(f)
        else:
            files_low.append(f) 

    

    # Start converting 
    # if len(files_low) == 4:
    #     print(f'Ready to convert {files_low} to 2.2.')
    #     convert(pack, files_low, "")

    # if len(files_medium) == 4:
    #     print(f'Ready to convert {files_medium} to 2.2.')
    #     convert(pack, files_medium, "-hd")

    # if len(files_high) == 4:
    #     print(f'Ready to convert {files_high} to 2.2.')
    #     convert(pack, files_high, "-uhd")

    # if len(files_low + files_medium + files_high) == 0:
    #     print(f'No files found!')
    # else:
    #     print(f"Converted textures are saved in {join(pack, 'output')}!")
    
    input("Press Enter to close the window.")

# you mean inconvennient practices smh
if __name__ == "__main__":
    main()