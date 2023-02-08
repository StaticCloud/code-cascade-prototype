from flask import Flask
from app.db import init_db;

def create_app(test_config=None):
    # create a new Flask object
    # tell Flask to serve static objects from the root directory
    app = Flask(__name__, static_url_path='/')
    # trailing slashes are optional (i.e. /dashboard === /dashboard/)
    app.url_map.strict_slashes = False
    # specify a key to use for creating server-side sessions
    app.config.from_mapping(
        SECRET_KEY='super_secret_key'
    )

    init_db(app)

    # activate the environment and run the Flask server using python -m flask run
    return app;