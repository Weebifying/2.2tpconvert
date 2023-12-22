import re
import plistlib
import os, sys
import traceback
import time
from PIL import Image
from os.path import join, isfile, isdir, splitext, abspath


def convert(dir, files, suffix):
    start_time = time.time()
    try:
        # Makes 2 folders: $dir/output and $dir/output/icons
        try:
            os.mkdir(join(dir, "output"))
        except:
            pass

        try:
            os.mkdir(join(dir, "output", "icons"))
        except:
            pass


        with open(join(dir, f"GJ_GameSheet02{suffix}.plist"), 'rb') as f:
            gs02_data = plistlib.load(f) 
            gs02_frames = list(gs02_data.get('frames').items())
        with open(join(dir, f"GJ_GameSheetGlow{suffix}.plist"), 'rb') as f:
            gsgl_data = plistlib.load(f)
            gsgl_frames = list(gsgl_data.get('frames').items())

        gs02_image = Image.open(join(dir, f"GJ_GameSheet02{suffix}.png"))
        gsgl_image = Image.open(join(dir, f"GJ_GameSheetGlow{suffix}.png"))

        sprites_list = []

        for key in gs02_frames:
            if key[0].startswith(('bird_', 'dart_', 'player_', 'robot_', 'ship_', 'spider_')):
                # Check if the sprite is of an icon to add in sprites_list
                if key[0].startswith('player_ball_'):
                    sprites_list.append(["player_ball_" + key[0].split("_")[2], []])
                else:
                    sprites_list.append([key[0].split("_")[0] + "_" + key[0].split("_")[1], []])

        # ??? what does this do
        res = []
        [res.append(x) for x in sprites_list if x not in res]
        sprites_list = res

        sprites_dict = {sub[0]: sub[1] for sub in sprites_list}

        # God I have no idea what's happening here
        for key in gs02_frames + gsgl_frames:
            if key[0].startswith(('bird_', 'dart_', 'player_', 'robot_', 'ship_', 'spider_')):
                if key[0].startswith('player_ball_'):
                    sprites_dict["player_ball_" + key[0].split("_")[2]].append(key)
                else:
                    # robtop made it so that some robots' glows can be found in both gamesheet02 and gamesheetglow for whatever reason
                    # so this is a thing to eliminate the extra glows
                    test = True
                    for testkey in sprites_dict[key[0].split("_")[0] + "_" + key[0].split("_")[1]]:
                        if key[0] == testkey[0]:
                            test = False
                    if test:
                        sprites_dict[key[0].split("_")[0] + "_" + key[0].split("_")[1]].append(key)


        # honestly idek how to describe this
        # just read it 
        for icon in sprites_dict:
            w = 0
            h = 0
            x = 0
            icon_frames = {}
            
            for key in sprites_dict[icon]:
                w += int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[0])) if not key[1]["textureRotated"] else int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[1]))
                w += 1 
                if h < int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[1])) and not key[1]["textureRotated"]:
                    h = int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[1]))
                elif h < int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[0])) and key[1]["textureRotated"]:
                    h = int(float(re.search("(?<={)(.*)(?=})", key[1]["spriteSize"]).group(1).split(',')[0]))
            sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0))

            for key in sprites_dict[icon]:
                left = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[0]))
                upper = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[1]))
                if key[1]["textureRotated"] == False:
                    right = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[0])) + int(float(re.search("(?<=,{)(.*)(?=}})", key[1]["textureRect"]).group(1).split(',')[0]))
                    lower = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[1])) + int(float(re.search("(?<=,{)(.*)(?=}})", key[1]["textureRect"]).group(1).split(',')[1]))
                else:
                    right = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[0])) + int(float(re.search("(?<=,{)(.*)(?=}})", key[1]["textureRect"]).group(1).split(',')[1]))
                    lower = int(float(re.search("(?<={{)(.*)(?=},)", key[1]["textureRect"]).group(1).split(',')[1])) + int(float(re.search("(?<=,{)(.*)(?=}})", key[1]["textureRect"]).group(1).split(',')[0]))
                

                if key[0].endswith("glow_001.png") and key[0].startswith(('bird_', 'dart_', 'player_', 'ship_')):
                    sprite = gsgl_image.crop((left, upper, right, lower))
                else:
                    sprite = gs02_image.crop((left, upper, right, lower))

                sheet.paste(sprite, (x, 0))

                key[1]["textureRect"] = "{{" + str(x) + "," + "0" + "},{" + str(sprite.width) + "," + str(sprite.height) + "}}"

                x += right - left + 1
                icon_frames[key[0]] = key[1]
                
            # plist metadata
            plist_data = {
                "frames": icon_frames, 
                "metadata": {
                    "format": 3,
                    "pixelFormat": "RGBA4444",
                    "premultiplyAlpha": False,
                    "realTextureFileName": "icons/" + splitext(icon)[0] + suffix + ".png",
                    "size": "{" + str(w) + "," + str(h) + "}",
                    "smartupdate": "",
                    "textureFileName": "icons/" + splitext(icon)[0] + suffix + ".png"
                }
            }

            # write the plist and png
            f = open(join(dir, "output", "icons", f"{splitext(icon)[0]}{suffix}.plist"), 'wb')
            plistlib.dump(plist_data, f)
            sheet.save(join(dir, "output", "icons", f"{splitext(icon)[0]}{suffix}.png"))
        
        print(f"Done! ({round(time.time() - start_time, 4)} seconds)")
    except Exception as e:
        print(f"An error occurred while converting {files}:")
        print(key)
        print(traceback.format_exc())   


def main():
    try:
        pack = abspath(input("Enter your 2.1 pack path: "))
        files_list = [f for f in os.listdir(pack) if isfile(join(pack, f))]
    except:
        # If the input is incorrect,
        # prints the erroe message and ask for input again
        print("Wrong/Invalid pack path!")
        print(traceback.format_exc())
        print()
        main()
        return "balls"

    files_low = []
    files_medium = []
    files_high = []

    # Separating between graphic types
    for f in files_list:
        if splitext(f)[0] in ['GJ_GameSheet02', 'GJ_GameSheetGlow'] and splitext(f)[1] in ['.plist', '.png']:
            files_low.append(f) 
        elif splitext(f)[0] in ['GJ_GameSheet02-hd', 'GJ_GameSheetGlow-hd'] and splitext(f)[1] in ['.plist', '.png']:
            files_medium.append(f)
        elif splitext(f)[0] in ['GJ_GameSheet02-uhd', 'GJ_GameSheetGlow-uhd'] and splitext(f)[1] in ['.plist', '.png']:
            files_high.append(f)

    # Start converting 
    if len(files_low) == 4:
        print(f'Ready to convert {files_low} to 2.2.')
        convert(pack, files_low, "")

    if len(files_medium) == 4:
        print(f'Ready to convert {files_medium} to 2.2.')
        convert(pack, files_medium, "-hd")

    if len(files_high) == 4:
        print(f'Ready to convert {files_high} to 2.2.')
        convert(pack, files_high, "-uhd")

    if len(files_low + files_medium + files_high) == 0:
        print(f'No files found!')
    else:
        print(f"Converted textures are saved in {join(pack, 'output')}!")
    
    input("Press Enter to close the window.")


main()