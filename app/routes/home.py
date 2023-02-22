from flask import Blueprint, render_template, session, redirect
from app.models import Article
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    # get all articles, sort them in descending order by creation date
    # obtain only the first five
    db = get_db()
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    articles = articles[:5]
    return render_template('home.html', articles=articles)