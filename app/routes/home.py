from flask import Blueprint, render_template, session, redirect
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('home.html')