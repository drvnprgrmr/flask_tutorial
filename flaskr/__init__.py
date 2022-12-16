import os

from flask import Flask


def create_app(test_config=None):
    # Define and create app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="key",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )
    
    if test_config is None:
        # Load config file if exists
        app.config.from_pyfile("config.py", silent=True)

    else:
        # Load test config
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Handle database 
    from . import db
    db.init_app(app)

    # Handle auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    # Handle blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
    
    
    return app