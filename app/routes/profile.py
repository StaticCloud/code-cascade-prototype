from flask import Blueprint, render_template, session, redirect
from app.models import User, Comment
from app.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', defaults={'id': None})
@bp.route('/<id>')
def dashboard(id):
    db = get_db()
    authUser = False

    try:
        if id == None:
            authUser = True
            user = db.query(User).filter(User.id == session.get('user_id')).one()
        else:
            if int(id) == session.get('user_id'):
                return redirect('/profile')
            else:
                user = db.query(User).filter(User.id == id).one()

        return render_template('profile.html', loggedIn=session.get('loggedIn'), user=user, authUser=authUser)
    except:
        return redirect('/profile')

@bp.route('/edit')
def edit():
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).one()

    return render_template('edit-profile.html', loggedIn=session.get('loggedIn'), user=user)