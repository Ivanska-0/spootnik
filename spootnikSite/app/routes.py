#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
import os
import sys
from math import trunc

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


@app.route("/ese_enlace")
def ese_enlace():
    return render_template("index/ese_enlace.html")


@app.route("/about")
def about():
    return render_template("index/about.html")
