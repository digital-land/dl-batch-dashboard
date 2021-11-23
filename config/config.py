# -*- coding: utf-8 -*-

import pathlib
import os
from datetime import timedelta


class Config(object):
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
    SECRET_KEY = os.getenv("SECRET_KEY")
    if (
        "AWS_ACCESS_KEY_ID" not in os.environ
        or "AWS_SECRET_ACCESS_KEY" not in os.environ
    ):
        raise KeyError("Missing AWS credential environment variables")


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
