#!/usr/bin/env python3

"""
This code trim your pictures and then converts them into spritesheet.

You need to:
1. Python 3
2. Pillow module
    pip3 install pillow

3. Add your images to "images_folder"
    The style of the name of the images should look like this:
    image_01.png, image_02.png, image_03.png, etc
4. Run code
5. Get trimmed images in "trims_folder"
6. Get your spritesheet from the folder where the code is in it. (root directory)

You could change the "COL_MAX" variable for the column number of spritesheet.
"""


from os import listdir
from PIL import Image
from time import strftime

images_folder = "images_folder/"
trims_folder = "trims_folder/"

COL_MAX = 7.0


def trimming():
    # Get a list of all files
    images = listdir(images_folder)
    im_frames = []
    
    for i in images: im_frames.append(i)

    # Get a list of image sizes
    sides = []
    
    for i in im_frames:
        im = Image.open(images_folder + i).getbbox()
        sides.append(im)

    # Get the min/max size of images
    sides_left = []
    sides_upper = []
    sides_right = []
    sides_lower = []
    
    for i in sides:
        sides_left.append(i[0])
        sides_upper.append(i[1])
        sides_right.append(i[2])
        sides_lower.append(i[3])

    limit_side_left = min(sides_left)
    limit_side_upper = min(sides_upper)
    limit_side_right = max(sides_right)
    limit_side_lower = max(sides_lower)

    # Trim and save trimmed images
    box = (limit_side_left, limit_side_upper, limit_side_right, limit_side_lower)
    dpi = Image.open(images_folder + im_frames[0]).info["dpi"]

    for i in im_frames:
        im = Image.open(images_folder + i).crop(box)
        im.save(trims_folder + i, dpi=dpi)
    
    print("Trimming is done!")
    pass


def spritesheet():
    # Get a list of files
    trims = listdir(trims_folder)
    tm_frames = []

    for i in trims:
        im = Image.open(trims_folder + i)
        tm_frames.append(im)
    
    # Get the height and width of one of them
    tile_width = tm_frames[0].size[0]
    tile_height = tm_frames[0].size[1]

    # Calculates the height and width of the spritesheet screen
    spritesheet_width = 0
    spritesheet_height = 0
    FRAME_MAX = len(tm_frames)
    frame_no = FRAME_MAX
    row_max = 1.0

    if FRAME_MAX <= COL_MAX:
        spritesheet_width = tile_width * FRAME_MAX
        spritesheet_height = tile_height
    elif FRAME_MAX > COL_MAX:
        for i in range(1, FRAME_MAX+1):
            if frame_no > COL_MAX:
                frame_no -= COL_MAX
                row_max += 1
        spritesheet_width = tile_width * COL_MAX
        spritesheet_height = tile_height * row_max
        
    # Make a blank page for spritesheet
    spritesheet = Image.new("RGBA", (int(spritesheet_width), int(spritesheet_height)))

    # Copy the trimmed images on the spritesheet
    left = 0
    upper = 0
    row_pointer = 1

    for i in trims:
        im = Image.open(trims_folder + i)
        spritesheet.paste(im, (left, upper))

        if FRAME_MAX <= COL_MAX:
            left += tile_width
        elif FRAME_MAX > COL_MAX:
            left += tile_width
            if row_pointer < row_max and left == tile_width * COL_MAX:
                left = 0
                upper += tile_height
                row_pointer += 1

    # Save spritesheet
    timestr = strftime("%Y-%m-%d_%H-%M-%S")
    dpi = tm_frames[0].info["dpi"]

    spritesheet.save("spritesheet_%s.png" % timestr, "PNG", dpi=dpi)

    print("spritesheet is done!")
    pass


trimming()
spritesheet()
