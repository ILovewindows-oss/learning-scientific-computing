# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.before_first_request
def load_global_data():
    """ Perform actions once during application startup. """
    pass


@app.route("/")
def index():
    """ Application entry point. """
    return render_template("index.html")


def create_app(config="flaskapp.config.Config"):
    """ Create application for server.

    This is the main function in the application, being responsible
    by the initialization of all internal engines, administration
    interfaces, data, encryption, mailing, and login. It will start
    by creating the main app, initializing the globals defined in
    this module, and then setting up the components by means of
    other methods provided in this module.

    Parameters
    ----------
    config_class : str
        String containing the access format for the configuration
        manager class. This allows for different parameters during
        development and production environments. Default is
        `"config.Config"`, situated in a Python module in the same
        level as the launcher.
    """
    global app

    app.config.from_object(config)
    
    return app
