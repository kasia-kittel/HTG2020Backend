import os
from flask_api import FlaskAPI


def create_app(test_config=None):

    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init the database
    from . import db
    db.init_app(app)

    # add blueprints
    from . import consumers
    app.register_blueprint(consumers.bp)

    from . import professionals
    app.register_blueprint(professionals.bp)

    # a healthcheck
    @app.route('/healthcheck')
    def healthcheck():
        return {'status': 'ok'}

    return app