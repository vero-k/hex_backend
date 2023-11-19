


def create_app(config=None):

    from flask import Flask
    app = Flask(__name__)

    from . import configurations

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(configurations.DevConfig)
    else:
        # load the test config if passed in
        app.config.from_object(configurations.TestConfig)
    
    import os
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flask_cors import CORS
    CORS(app)

    from .db_module import get_db, db_exists, init_db, close_db
    db = initialize_database(app, get_db, db_exists, init_db)

    from .routes import player
    app.register_blueprint(player.playr)

    from .routes import game
    app.register_blueprint(game.game)


    @app.route("/testit")
    def testit():
        return "test it"


    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
        return "teardown"


    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist', 404


    return app



def initialize_database(app, get_db, db_exists, init_db):
    with app.app_context():
        if db_exists():
            return get_db()
        else:
            return init_db()
