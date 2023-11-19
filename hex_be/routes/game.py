
import os
import shutil

from ..db_module import get_db
from ..configurations import Config

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response, jsonify, make_response, send_from_directory
)

from werkzeug.utils import secure_filename
from PIL import Image

from ..util.grid import gridIt, gridIt_mods



game = Blueprint("game", __name__)

    

@game.route("/post-image/", methods=["POST"])
def post_image():
    image = request.files.get('file')   # FileStorage Object, 
    belongs_to_player_id = request.form["userID"]
    level = int(request.form["level"])
    difficulty = request.form["difficulty"]
    org_width = int(request.form["orgWidth"])
    org_height = int(request.form["orgHeight"])
    width = int(request.form["width"])
    height = int(request.form["height"])
    top = int(request.form["top"])
    left = int(request.form["left"])
    hex_nr_width = int(request.form["hexNrWidth"])
    hex_nr_height = int(request.form["hexNrHeight"])


    upload_dir_base = Config.UPLOAD_DIR_BASE

    file_name = secure_filename(belongs_to_player_id + '.jpg')
    
    upload_file_path = os.path.join(upload_dir_base, file_name)
    
    base_img = Image.open(image)
    base_img.crop((left, top, left + width, top + height))
    base_img.save(upload_file_path)

    query_str = '''INSERT INTO game(level, difficulty, width, height, hex_nr_width, hex_nr_height, belongs_to_player_id) VALUES(?, ?, ?, ?, ?, ?, ?)'''
    query_tuple = (level, difficulty, width, height, hex_nr_width, hex_nr_height, belongs_to_player_id, )

    con = get_db()
    cur = con.cursor()
    cur.execute(query_str, query_tuple)
    con.commit()

    game_id = cur.lastrowid

    query_str = '''INSERT INTO playergame(player_id, game_id) VALUES(?, ?)'''
    query_tuple = (belongs_to_player_id, game_id)

    cur.execute(query_str, query_tuple)
    con.commit()

    response = jsonify({'game_id': game_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@game.route("/grid-image/", methods=["GET"])
def gridimage():

    con = get_db()
    cur = con.cursor()

    game_id = request.args.get('gameID')

    query_str = '''SELECT * FROM game WHERE id = ?'''
    cur.execute(query_str, (game_id,))
    con.commit()
    (id, level, difficulty, width, height, hex_nr_width, hex_nr_height, belongs_to_player_id, ) = cur.fetchone()

    path_arr = []

    upload_dir_base = Config.UPLOAD_DIR_BASE
    upload_dir_raster = Config.UPLOAD_DIR_RASTER

    file_name = secure_filename(str(belongs_to_player_id) + '.jpg')
    new_dir_name = secure_filename(str(belongs_to_player_id))
    
    download_base_img = os.path.join(upload_dir_base, file_name)
    base_img = Image.open(download_base_img)

    upload_raster = os.path.join(upload_dir_raster, new_dir_name)
    path_arr.append(upload_raster)

    if not os.path.exists(upload_raster):
        os.makedirs(upload_raster)

    for i in range(0, level):
        dir_path = Config.UPLOAD_DIR_LEVEL[i]
        new_dir = os.path.join(dir_path, new_dir_name)
        path_arr.append(new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    mod_tracker = gridIt_mods(width, height, hex_nr_width, hex_nr_height, base_img, path_arr, level, difficulty)

    response = jsonify(mod_tracker)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@game.route("/get-image/", methods=["GET"])
def getimage():


    game_id = request.args.get('gameID')
    user_id = request.args.get('userID')

    current_img = request.args.get('currentImg') + '.jpg'

    #upload_dir_raster = "hex_be" + Config.UPLOAD_DIR_RASTER_DONE

    #new_dir = secure_filename(user_id)
    #file_name = secure_filename(current_img + ".jpg")

    #upload_raster = os.path.join(upload_dir_raster, new_dir)
    # path_to_img = os.path.join('', current_img + '.jpg')
    # print(path_to_img)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_directory = os.path.join(BASE_DIR, 'static', 'images', 'rastered', user_id)
    path_to_img = os.path.join(images_directory, current_img)

    sf = send_from_directory(images_directory, current_img)
    response = make_response(sf)
    response.headers['Access-Contol-Allow-Origin'] = '*'
    return response
  




@game.route("/get-image-mods/", methods=["GET"])
def getimagemods():

    game_id = request.args.get('gameID')
    user_id = request.args.get('userID')

    current_img = request.args.get('currentImg') + '.jpg'
    layer = int(request.args.get('layer')) - 1
    #upload_dir_raster = "hex_be" + Config.UPLOAD_DIR_RASTER_DONE

    #new_dir = secure_filename(user_id)
    #file_name = secure_filename(current_img + ".jpg")

    #upload_raster = os.path.join(upload_dir_raster, new_dir)
    # path_to_img = os.path.join('', current_img + '.jpg')
    # print(path_to_img)
    upload_dir_raster = Config.UPLOAD_DIR_LEVEL_DONE[layer]

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_directory = os.path.join(BASE_DIR, 'static', 'images', upload_dir_raster, user_id)
    path_to_img = os.path.join(images_directory, current_img)

    sf = send_from_directory(images_directory, current_img)
    response = make_response(sf)
    response.headers['Access-Contol-Allow-Origin'] = '*'
    return response

    


@game.route("/erase/<int:id>")
def erase(id):
    folder = 'static/rastered/' + id
    success = True
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            
        except Exception as e:
            success = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    folder = 'static/levelone/' + id
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            
        except Exception as e:
            success = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    folder = 'static/baseimg/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename == id:
                os.unlink(file_path)
            
        except Exception as e:
            success = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    response = jsonify({'deleted': success})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response