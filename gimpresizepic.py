#!/usr/bin/env python

from gimpfu import gimp, pdb, register, PF_FILENAME, PF_SPINNER, main
from os import path


def resize_img(img, percent, new_path):
    img2 = pdb.gimp_image_duplicate(img)
    new_width = int(round(img2.width * percent / 100.0))
    new_height = int(round(img2.height * percent / 100.0))
    pdb.gimp_image_scale(img2, new_width, new_height)
    pdb.file_jpeg_save(img2, img2.layers[0], new_path, new_path,
                        0.95, 0, 0, 0, "Created with GIMP", 0, 0, 0, 0)
    return [path.getsize(new_path) / 1024.0, new_width]


def kb_resize(picture_path, kb_size):
    size1 = path.getsize(picture_path) / 1024.0
    eps = 1
    if size1 < kb_size:
        gimp.message('File size already smaller than %d kb' % kb_size)
        return

    new_path = "%s_resized.jpg" % path.splitext(picture_path)[0]
    if picture_path.lower().endswith(".png"):
        try:
            img = pdb.file_png_load(picture_path, picture_path)
        except:
            img = pdb.file_jpeg_load(picture_path, picture_path)
    elif picture_path.lower().endswith((".jpeg", ".jpg")):
        try:
            img = pdb.file_jpeg_load(picture_path, picture_path)
        except:
            img = pdb.file_png_load(picture_path, picture_path)
    else:
        gimp.message("Problem with %s" % picture_path)
        return
    if not img:
        gimp.message("Problem with %s" % picture_path)
        return
    p1 = 0.0
    p2 = 100.0
    size = size1
    width_list = []
    while (size < kb_size - eps) or (size > kb_size):
        percent = (p1 + p2)/2.0
        # [size, w] = fct_resize(picture_path, percent)
        [size, w] = resize_img(img, percent, new_path)
        if (w in width_list) and (size < kb_size):
            break
        width_list.append(w)
        if size < 0:
            gimp.message("Problem with %s" % picture_path)
            return
        if size < kb_size:
            p1 = (p1 + p2)/2.0
        else:
            p2 = (p1 + p2)/2.0

register(
    "python_fu_kbresize",
    "Resize to wished size in kB",
    "Resize to wished size in kB (iteratively)",
    "A. Domi",
    "A. Domi",
    "2016",
    "Resize image (py)",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_FILENAME, "picture_path", "Picture file to resize", path.expanduser("~")),    # Choose a file
        (PF_SPINNER, "kb_size", "Size [kB]", 250, (10, 51200, 1))
    ],
    [],
    kb_resize, menu="<Image>/File")

main()
