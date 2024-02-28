
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response, jsonify
)

from ..db_module import get_db


playr = Blueprint("playr", __name__)

@playr.route('/test/')
def testplayer():
    return jsonify({"message": "ok"}), 200
    


@playr.route('/newplayer/')
def newplayer():
    name = request.args.get('name', 'anonymous')
    try:
        db = get_db()
        cursor = db.execute("INSERT INTO player (name) VALUES (?)", (name,),)
        db.commit()
        return jsonify({"id": cursor.lastrowid})
    except db.IntegrityError:
        error = f"error"
        flash(error)
        return jsonify({"error": error}), 400
