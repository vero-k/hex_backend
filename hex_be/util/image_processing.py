
import random, math, os
from PIL import Image, ImageFilter, ImageColor, ImageOps, ImageChops



MODIFICATION_OPERATIONS = ['rotate', 'mirror', 'blend', 'colorinvert', 'blur', 'deform', 'cat']
MODIFICATION_NUMBER = 7




class SingleDeformer:

    def getmesh(self, img):
        #Map a target rectangle onto a source quad
        return [(
                # target rectangle
                (200, 100, 300, 200),
                # corresponding source quadrilateral
                (0, 0, 0, 100, 100, 200, 100, 0)
                )]



def mod_img(img):
    
    mod_img = None
    op = MODIFICATION_OPERATIONS[math.floor(random.uniform(0, 1) * MODIFICATION_NUMBER)]

    if op == 'rotate':
        angle = random.randint(20, 340)
        mod_img = img.rotate(angle)
    elif op == 'mirror':
        mod_img = ImageOps.mirror(img)
    elif op == 'blend':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_directory = os.path.join(BASE_DIR, 'static', 'images', 'icons')
        path_to_img = os.path.join(icon_directory, 'kitty.png')
        cat_img = Image.open(path_to_img)
        width, height = img.size
        cat_img = cat_img.crop((0, 0, width, height))
        mod_img = Image.blend(img, cat_img, 0.5)
    elif op == 'deform':
        mod_img = ImageOps.deform(img, SingleDeformer())
    elif op == 'blur':
        mod_img = img.filter(ImageFilter.GaussianBlur(radius=5))
    elif op == 'colorinvert':
        mod_img = ImageChops.invert(img)
    elif op == 'cat':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_directory = os.path.join(BASE_DIR, 'static', 'images', 'icons')
        path_to_img = os.path.join(icon_directory, 'kitty.png')
        cat_img = Image.open(path_to_img)
        width, height = img.size
        cat_img = cat_img.crop((0, 0, width, height))
        mod_img = cat_img

    # elif op == 'twocolor':
    #     r = random.randint(0, 255)
    #     g = random.randint(0, 255)
    #     b = random.randint(0, 255)
    #     rgb1 = [r,g,b]
    #     r = random.randint(0, 255)
    #     g = random.randint(0, 255)
    #     b = random.randint(0, 255)
    #     rgb2 = [r,g,b]
    #     mod_img = ImageOps.colorize(img, rgb1, rgb2)

    return (mod_img, op)
    





