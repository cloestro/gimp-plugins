#!/usr/bin/env python

# Hello World in GIMP Python

from gimpfu import *



def hello_world(initstr, font, size, color, width, height):
    # First do a quick sanity check on the font
    if font == 'Comic Sans MS' :
        initstr = "Comic Sans? Are you sure?"

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

    # Create a new image window
    gimp.Display(img)
    # Show the new image window
    gimp.displays_flush()

    # Restore the old foreground color:
    pdb.gimp_context_pop()

register(
    "python_fu_add_text",
    "Add text to image",
    "Create a new image with your text string",
    "Domi",
    "Domi",
    "2016",
    "Create transparent image with text (py)...",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "Text string", 'Hello, world!'),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 50, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (1.0, 1.0, 1.0)),
        (PF_SPINNER, "width", "Width", 1920, (1, 10000, 1)),
        (PF_SPINNER, "height", "Height", 1080, (1, 10000, 1))
    ],
    [],
    hello_world, menu="<Image>/File")

main()
