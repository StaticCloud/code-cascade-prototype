from flask import Blueprint, render_template, session, redirect, request
from app.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
def dashboard():
    return render_template('profile.html', loggedIn=session.get('loggedIn'))