#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from werkzeug.urls import url_parse
from flask import render_template, request, url_for, redirect, session, flash
import os
import sys
from math import trunc
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

load_dotenv()
ENLACE_SECRET = os.getenv("ENLACE_SECRET")

# Directorios
ROOT = os.path.dirname(__file__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/imperium")
def imperium():
    return render_template("index/imperium.html")


@app.route("/fitos")
def fitos():
    return render_template("index/fitos.html")

@app.route("/residuos")
def residuos():
    return render_template("residuos/index.html")


@app.route("/ese_enlace", methods=["GET", "POST"])
def ese_enlace():
    if "pass" in request.form and \
            check_password_hash(ENLACE_SECRET, request.form["pass"]):
        return render_template("index/aaa.html")

    return render_template("index/ese_enlace.html")


@app.route("/about")
def about():
    return render_template("index/about.html")
