from flask import Blueprint, render_template, session, redirect, request
from sqlalchemy import and_, extract
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
    return render_template('home.html', articles=articles, loggedIn=session.get('loggedIn'))

@bp.route('/search')
def search():
    db = get_db()
    args = request.args.to_dict();

    if not args:
        return render_template('search.html', loggedIn=session.get('loggedIn'))
    
    filters = []

    if args.get('year'):
        filters.append(extract('year', Article.created_at) == args.get('year'))

    if args.get('category'):
        filters.append(Article.category == args.get('category'))

    if args.get('keywords'):
        args['keywords'] = args.get('keywords').split('+')

        for keyword in args.get('keywords'):
            filters.append(Article.title.contains(keyword))

    articles = db.query(Article).filter(and_(*filters)).all()
    
    return render_template('search-results.html', keywords=args.get('keywords'), articles=articles, loggedIn=session.get('loggedIn'))
    
@bp.route('/article/<id>')
def article(id):
    db = get_db()
    article = db.query(Article).filter(Article.id == id).one();
    is_liked = False;

    for like in article.likes:
        if like.user_id == session.get('user_id'):
            is_liked = True;

    return render_template('article.html', article=article, is_liked=is_liked)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')