#!/usr/bin/env python

# Hello World in GIMP Python

from math import log10
from gimpfu import *

def create_pngs(txtpath, font, size, color, width, height):
    dirname = r'C:\Users\msiy4w\Pictures\Wallpapers_out'
    f = open(txtpath, 'r')
    L = f.readlines()
    i = 0
    f.close()
    fmt_nb = int(log10(len(L))) + 1
    for l in L:
        if l.strip():
            i += 1

            pngname = "%s/pic_%s.png" % (dirname, str(i).zfill(fmt_nb))
            hello_world(l.strip(), font, size, color, width, height, pngname)

def hello_world(initstr, font, size, color, width, height, pngname):

    # Make a new image. Size 10x10 for now -- we'll resize later.
    img = gimp.Image(int(width), int(height), RGB)

    # Save the current foreground color:
    pdb.gimp_context_push()

    # Set the text color
    gimp.set_foreground(color)

    # Create a new text layer (-1 for the layer means create a new layer)
    layer = pdb.gimp_text_fontname(img, None, 0, 0, initstr, 10,
                                   True, size, PIXELS, font)

    layer.translate(int(0.075 * img.width), int(0.85 * img.height))
    # Resize the image to the size of the layer
    #img.resize(layer.width, layer.height, 0, 0)

    # Background layer.
    # Can't add this first because we don't know the size of the text layer.
    background = gimp.Layer(img, "Background", img.width, img.height,
                            RGBA_IMAGE, 100, NORMAL_MODE)
    background.fill(TRANSPARENT_FILL)
    img.add_layer(background, 1)

    # Restore the old foreground color:
    pdb.gimp_context_pop()

    layer_merged = pdb.gimp_image_merge_visible_layers(img, CLIP_TO_IMAGE)
    pdb.file_png_save(img, layer_merged, pngname, pngname, 0, 9, 0, 0, 0, 0, 0)


register(
    "python_fu_txt2pngs",
    "Put txt in pngs",
    "Create a new image with your text string",
    "Anthony Domi",
    "Anthony Domi",
    "2016",
    "Put .txt in pngs (py)...",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "txt path", 'C:/users/msiy4w/Desktop/test.txt'),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 50, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (1.0, 1.0, 1.0)),
        (PF_SPINNER, "width", "Width", 1920, (1, 10000, 1)),
        (PF_SPINNER, "height", "Height", 1080, (1, 10000, 1))
    ],
    [],
    create_pngs, menu="<Image>/File")

main()
