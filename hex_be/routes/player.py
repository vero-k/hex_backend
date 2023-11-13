
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response,
)

playr = Blueprint("playr", __name__)


@playr.before_app_request
def load_player():
    player_id = session.get('player_id')

    if player_id is None:
        g.player = None
    else:
        g.player = get_db().execute(
            'SELECT * FROM player WHERE player_id = ?', (player_id,)
        ).fetchone()



@playr.route('/exit')
def logout():
    session.clear()
    return redirect(url_for('index'))


@playr.route('/name', methods=('GET', 'POST'))
def name():
    if request.method == 'POST':
        player_name = request.form['playername']
        db = get_db()
        error = None

        if not playername:
            error = 'Player name is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO player (player_name) VALUES (?)",
                    (player_name),
                )
                db.commit()
            except db.IntegrityError:
                error = f"error"
            else:
                return "ok"

        flash(error)
        response = jsonify({"success": True})

    return render_template('auth/register.html')