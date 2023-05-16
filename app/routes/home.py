from flask import Blueprint, render_template, session, redirect, request
from sqlalchemy import and_, extract
from app.models import Article, Comment
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
    
# calculate the comment depth
def commentDepth(comment, depth):
    comment.depth = depth;
    for reply in comment.replies:
        commentDepth(reply, depth + 1)

@bp.route('/article/<id>')
def article(id):
    db = get_db()
    article = db.query(Article).filter(Article.id == id).one();
    is_liked = False;
    is_saved = False;

    for like in article.likes:
        if like.user_id == session.get('user_id'):
            is_liked = True;
    
    for save in article.saves:
        if save.user_id == session.get('user_id'):
            is_saved = True;
    
    article.replies = [reply for reply in article.replies if reply.parent_comment == None]

    for reply in article.replies:
        commentDepth(reply, 0)

    return render_template('article.html', article=article, is_liked=is_liked, is_saved=is_saved, loggedIn=session.get('loggedIn'), avatar=session.get('avatar'))

@bp.route('/comment/<id>')
def comment(id):
    db = get_db()

    # try:
    comment = db.query(Comment).where(Comment.id == id).one()
    comment.depth = 0;

    for reply in comment.replies:
        commentDepth(reply, 1)

    return render_template('comment-page.html', comment=comment, loggedIn=session.get('loggedIn'), avatar=session.get('avatar'))
    # except:
    #     return redirect('/')
    
@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')