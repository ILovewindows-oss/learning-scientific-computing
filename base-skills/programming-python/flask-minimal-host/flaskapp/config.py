# -*- coding: utf-8 -*-
import os


class Config:
    """ Retrieve configurations from environment. """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    """ Main application encryption key. """

    WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", True)
    """ Enable CSRF protection. """
