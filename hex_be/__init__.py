from flask import Flask, request, jsonify, make_response, g, send_file, current_app
from flask_cors import CORS
from werkzeug.utils import secure_filename


from PIL import Image, ImageFilter

import os, sys
from datetime import datetime
import base64
import shutil
from io import BytesIO
import pathlib

from .db import init_app, get_db
from .grid import gridIt, gridIt_mods


app = Flask(__name__, static_folder='')

CORS(app)


app.config["UPLOAD_DIR_BASE"] = 'hex_be/images/baseimg/'
app.config["UPLOAD_DIR_RASTER"] = 'hex_be/images/rastered/'
app.config["UPLOAD_DIR_LEVEL"] = ['hex_be/images/levelone/', 'hex_be/images/leveltwo/', 'hex_be/images/levelthree/']
app.config["UPLOAD_DIR_RASTER_DONE"] = 'images/rastered/'
app.config["UPLOAD_DIR_LEVEL_DONE"] = ['images/levelone/', 'images/leveltwo/', 'images/levelthree/']


with app.app_context():
    init_app(app)


@app.route("/testit")
def testit():
    return "test it"




@app.route("/postImage/", methods=['POST'])
def rasterize():
    print("inside post image")

    image = request.files.get('file')   # FileStorage Object, 

    user_id = request.form["userID"]
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


    upload_dir_base = app.config["UPLOAD_DIR_BASE"]

    file_name = secure_filename(user_id + '.jpg')
    
    upload_file_path = os.path.join(upload_dir_base, file_name)
    
    base_img = Image.open(image)
    base_img.crop((left, top, left + width, top + height))
    base_img.save(upload_file_path)

    query_str = '''INSERT INTO player(user_id, levl, difficulty, width, height, hex_nr_width, hex_nr_height) VALUES(?, ?, ?, ?, ?, ?, ?)'''
    query_tuple = (user_id, level, difficulty, width, height, hex_nr_width, hex_nr_height)

    con = get_db()
    cur = con.cursor()
    cur.execute(query_str, query_tuple)
    con.commit()

    
    # load, resize, crop
    response = jsonify({'some': file_name})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/gridImage/", methods=['GET'])
def gridimage():

    cur = get_db().cursor()

    user_id = request.args.get('userID')

    query_str = '''SELECT * FROM player WHERE user_id = ?'''
    cur.execute(query_str, (user_id,))
    (id, user_id, level, difficulty, width, height, hex_nr_width, hex_nr_height) = cur.fetchone()

    path_arr = []

    upload_dir_base = app.config["UPLOAD_DIR_BASE"]
    upload_dir_raster = app.config["UPLOAD_DIR_RASTER"]

    file_name = secure_filename(user_id + '.jpg')
    new_dir_name = secure_filename(user_id)
    
    download_base_img = os.path.join(upload_dir_base, file_name)
    base_img = Image.open(download_base_img)

    upload_raster = os.path.join(upload_dir_raster, new_dir_name)
    path_arr.append(upload_raster)

    if not os.path.exists(upload_raster):
        os.makedirs(upload_raster)

    for i in range(0, level):
        dir_path = app.config["UPLOAD_DIR_LEVEL"][i]
        new_dir = os.path.join(dir_path, new_dir_name)
        path_arr.append(new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    mod_tracker = gridIt_mods(width, height, hex_nr_width, hex_nr_height, base_img, path_arr, level, difficulty)

    response = jsonify(mod_tracker)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@app.route("/getImage/", methods=['GET'])
def getimage():

    user_id = request.args.get('userID')
    current_img = request.args.get('currentImg')

    upload_dir_raster = app.config["UPLOAD_DIR_RASTER_DONE"]

    new_dir = secure_filename(user_id)
    file_name = secure_filename(current_img + ".jpg")

    upload_raster = os.path.join(upload_dir_raster, new_dir)
    path_to_img = os.path.join(upload_raster, file_name)

    return send_file(path_to_img, mimetype='image/jpg')


@app.route("/getImageMods/", methods=['GET'])
def getimagemods():

    user_id = request.args.get('userID')
    current_img = request.args.get('currentImg')
    layer = int(request.args.get('layer'))

    upload_dir_raster = app.config["UPLOAD_DIR_LEVEL_DONE"][layer-1]
    new_dir = secure_filename(user_id)

    file_name = secure_filename(current_img + ".jpg")

    upload_raster = os.path.join(upload_dir_raster, new_dir)
    path_to_img = os.path.join(upload_raster, file_name)

    return send_file(path_to_img, mimetype='image/jpg')






@app.route("/rasterize/", methods=['POST'])
def rasterizeold():
    print("inside")

    image = request.files.get('file')   # FileStorage Object, 

    level = 1
    user_id = request.form["userID"]
    old_width = int(request.form["oldWidth"])
    old_height = int(request.form["oldHeight"])
    new_width = int(request.form["newWidth"])
    new_height = int(request.form["newHeight"])
    hex_nr_width = int(request.form["hexNrWidth"])
    hex_nr_height = int(request.form["hexNrHeight"])


    upload_dir_base = app.config["UPLOAD_DIR_BASE"]
    upload_dir_raster = app.config["UPLOAD_DIR_RASTER"]

    file_name = secure_filename(user_id + '.jpg')
    new_dir = secure_filename(user_id + '/')
    
    upload_file_path = os.path.join(upload_dir_base, file_name)
    upload_raster = os.path.join(upload_dir_raster, new_dir)

    if not os.path.exists(upload_raster):
        os.makedirs(upload_raster)
    
    base_img = Image.open(image)
    base_img.save(upload_file_path)


    query_str = '''INSERT INTO player(user_id, levl, img_old_width, img_old_height, img_new_width, img_new_height, hex_nr_width, hex_nr_height, base_img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    query_tuple = (user_id, level, old_width, old_height, new_width, new_height, hex_nr_width, hex_nr_height, upload_raster)

    con = get_db()
    cur = con.cursor()
    cur.execute(query_str, query_tuple)
    con.commit()


    gridIt(new_width, new_height, hex_nr_width, hex_nr_height, base_img, upload_raster)

    # load, resize, crop
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/erase", methods=['POST'])
def erase():
    user_id = request.json()['user']
    folder = 'static/rastered/' + user
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


    folder = 'static/levelone/' + user
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
            if os.path.isfile(file_path) or os.path.islink(file_path) and filename == user_id:
                os.unlink(file_path)
            
        except Exception as e:
            success = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    response = jsonify({'deleted': success})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


