import math
import base64
import shutil
import pathlib
import os
import random

from werkzeug.utils import send_file, secure_filename
from io import BytesIO

from PIL import Image, ImageFilter, ImageColor, ImageOps, ImageChops

from .image_processing import mod_img


MOD_RATE = {
    'easy': 0.3,
    'normal': 0.45,
    'advanced': 0.65,
    'hard': 0.8,
    'expert': 1
}


# mod_tracker is a dictionary. mapping keys (1 ... nr_hex in string format) to an array of values ('original', ...)
# array has 1 + max(level) entries 
def gridIt_mods(img_width: int, img_height: int, hex_nr_width: int, hex_nr_height: int, img: Image, path_arr: str, level: int, difficulty: str):

        mod_rate = MOD_RATE[difficulty]

        mod_tracker = {}

        nr_hex = hex_nr_height * hex_nr_width

        for l in range(nr_hex):
            mod_tracker[str(l)] = ['original']
        

        hex_rad = math.floor(min(img_width / hex_nr_width, img_height / hex_nr_height) / 2.0)

        hex_width = 2 * hex_rad
        hex_height = math.floor(math.sqrt(3) * hex_rad)

        horizontal_spacing = math.floor(hex_width * (3.0 / 4.0))
        vertical_spacing = hex_height
        
        horizontal_unit = math.floor(hex_rad / 2.0)
        vertical_unit = math.floor(hex_height / 2.0)

        nr_horizontal_units = math.floor(img_width / (horizontal_unit * 1.0))
        nr_vertical_units = math.floor(img_height / (vertical_unit * 1.0))

        current_ind = 0
        current_left = - horizontal_spacing


        for w in range(hex_nr_width):

            current_left = current_left + horizontal_spacing
            current_right = current_left + hex_width

            current_top = 0 if (w % 2 == 0) else vertical_unit
            current_bottom = current_top + hex_height


            for h in range(hex_nr_height):

                file_name = secure_filename(str(current_ind) + '.jpg')
                upload_file_path = os.path.join(path_arr[0], file_name)

                # crop and rotate, and save original
                bleed = math.floor((hex_width - hex_height) / 2)

                cropped_img = img.crop((current_left, current_top - bleed, current_right, current_bottom + bleed))
                
                bigger_img = Image.new('RGB', (hex_width, hex_width), "white")
                offset = (0, math.floor((hex_width - hex_height) / 2))

                bigger_img.paste(cropped_img, offset)

                rotated_img = bigger_img.rotate(120)

                rotated_img.save(upload_file_path)

                next_mod = rotated_img
                for l in range(0, level):

                    randNr = random.uniform(0, 1)
                    if randNr < mod_rate:

                        (next_mod, mod_name) = mod_img(next_mod)
                        mod_tracker.get(str(current_ind)).append(mod_name)

                        upload_file_path = os.path.join(path_arr[l+1], file_name)
                        next_mod.save(upload_file_path)
                    else:
                        break



                # calculate next crop border and index

                current_left = current_left
                current_right = current_right

                current_top = current_top + hex_height
                current_bottom = current_bottom + hex_height
                
                
                current_ind = current_ind + 1

        return mod_tracker



def gridIt_2(img_width: int, img_height: int, hex_nr_width: int, hex_nr_height: int, img: Image, path_arr: str, level: int, difficulty: str):

        mod_rate = MOD_RATE[difficulty]

        mod_tracker = {}

        nr_hex = hex_nr_height * hex_nr_width

        for l in range(nr_hex):
            mod_tracker[str(l)] = ['original']
        

        hex_rad = math.floor(min(img_width / hex_nr_width, img_height / hex_nr_height) / 2.0)

        hex_width = 2 * hex_rad
        hex_height = math.floor(math.sqrt(3) * hex_rad)

        horizontal_spacing = math.floor(hex_width * (3.0 / 4.0))
        vertical_spacing = hex_height
        
        horizontal_unit = math.floor(hex_rad / 2.0)
        vertical_unit = math.floor(hex_height / 2.0)

        nr_horizontal_units = math.floor(img_width / (horizontal_unit * 1.0))
        nr_vertical_units = math.floor(img_height / (vertical_unit * 1.0))

        current_ind = 0
        current_left = - hex_width


        for w in range(hex_nr_width):

            current_left = current_left + hex_width
            current_right = current_left + hex_width

            current_top = 0 if (w % 2 == 0) else horizontal_unit
            current_bottom = current_top + hex_height


            for h in range(hex_nr_height):

                file_name = secure_filename(str(current_ind) + '.jpg')
                upload_file_path = os.path.join(path_arr[0], file_name)

                # crop and rotate, and save original

                cropped_img = img.crop((current_left, current_top, current_right, current_bottom))

                cropped_img.save(upload_file_path)

                next_mod = cropped_img
                for l in range(0, level):

                    randNr = random.uniform(0, 1)
                    if randNr < mod_rate:

                        (next_mod, mod_name) = mod_img(next_mod)
                        mod_tracker.get(str(current_ind)).append(mod_name)

                        upload_file_path = os.path.join(path_arr[l+1], file_name)
                        next_mod.save(upload_file_path)
                    else:
                        break



                # calculate next crop border and index

                current_left = current_left
                current_right = current_right

                current_top = current_top + hex_height
                current_bottom = current_bottom + hex_height
                
                
                current_ind = current_ind + 1

        return mod_tracker





def gridIt(img_width: int, img_height: int, hex_nr_width: int, hex_nr_height: int, img: Image, storage_path: str):

        nr_hex = hex_nr_height * hex_nr_width

        hex_rad = math.floor(min(img_width / hex_nr_width, img_height / hex_nr_height) / 2.0)

        hex_width = 2 * hex_rad
        hex_height = math.floor(math.sqrt(3) * hex_rad)

        horizontal_spacing = math.floor(hex_width * (3.0 / 4.0))
        vertical_spacing = hex_height
        
        horizontal_unit = math.floor(hex_rad / 2.0)
        vertical_unit = math.floor(hex_height / 2.0)

        nr_horizontal_units = math.floor(img_width / (horizontal_unit * 1.0))
        nr_vertical_units = math.floor(img_height / (vertical_unit * 1.0))

        current_ind = 0
        current_left = - hex_width


        for w in range(hex_nr_width):

            current_left = current_left + hex_width
            current_right = current_left + hex_width

            current_top = 0 if (w % 2 == 0) else horizontal_unit
            current_bottom = current_top + hex_height


            for h in range(hex_nr_height):

                file_name = secure_filename(str(current_ind) + '.jpg')
                upload_file_path = os.path.join(storage_path, file_name)

                # crop and rotate, and save original

                cropped_img = img.crop((current_left, current_top, current_right, current_bottom))
                rot_img = cropped_img.rotate(120)
                rot_img.save(upload_file_path)


                # calculate next crop border and index

                current_left = current_left
                current_right = current_right

                current_top = current_top + hex_height
                current_bottom = current_bottom + hex_height
                
                
                current_ind = current_ind + 1

        return True


