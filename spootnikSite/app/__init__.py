#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_session import Session
import os
import sys
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

try:
    from flask_session import Session
    this_dir = os.path.dirname(os.path.abspath(__file__))
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = this_dir + '/thesessions'
    SESSION_COOKIE_NAME = 'flasksessionid'
    app.config.from_object(__name__)
    Session(app)
    sys.stderr.write("Usando sesiones de Flask-Session en fichero del servidor\n")
except ImportError as e:
    sys.stderr.write("Flask-Session no disponible, usando sesiones de Flask en cookie")


from app import routes
