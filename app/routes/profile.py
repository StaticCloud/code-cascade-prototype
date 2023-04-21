from flask import Blueprint, render_template, session
from app.models import User
from app.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
def dashboard():
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).one()

    return render_template('profile.html', loggedIn=session.get('loggedIn'), user=user)

@bp.route('/edit')
def edit():
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).one()

    return render_template('edit-profile.html', loggedIn=session.get('loggedIn'), user=user)