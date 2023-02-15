import sys
from flask import Blueprint, request, jsonify, session
from app.models import Comment, Article, User
from app.utils.auth import login_required
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

def getAllReplies(parent_reply):
    replies = [];
    if parent_reply.replies:
        for reply in parent_reply.replies:

            nested_replies = getAllReplies(reply)

            replies.append({
                "id": reply.id,
                "author": reply.author.username,
                "comment_text": reply.comment_text,
                "replies": nested_replies
            })

    return replies




@bp.route('/comment/<id>', methods=['GET'])
def comments(id):
    db = get_db()
    # query comments
    comments = db.query(Comment).filter(Comment.article_id == id).order_by(Comment.created_at.desc()).all()
    return {
        # return data formatted as JSON object
        'comments': [
            {
                # return comment text and replies for top-level comments
                'comment_text': comment.comment_text,
                'author': comment.author.username,
                'replies': [
                    {
                        # return the id, comment text, and nested replies for each reply
                        "id": reply.id,
                        "author": reply.author.username,
                        "comment_text": reply.comment_text,
                        "replies": getAllReplies(reply) # recursive function to iterate through nested replies
                    }
                    for reply in comment.replies # iterate through comment replies
                ]
            }
            for comment in comments # iterate through all top level comments
        ]
    }

@bp.route('/article/<id>', methods=['GET'])
def articles(id):
    db = get_db()
    article = db.query(Article).filter(Article.id == id).order_by(Article.created_at.desc()).one()
    return {
            'author': article.author.username,
            'title': article.title,
            'category': article.category,
            'likes': [
                {
                    'username': like.user.username,
                }
                for like in article.likes
            ],
            'replies': [
                {
                    'comment': reply.comment_text
                }
                for reply in article.replies
            ]
        }

@bp.route('/article', methods=['POST'])
def addArticle():
    data = request.get_json()
    db = get_db()

    try:
        article = Article(
            title = data.get('title'),
            category = data.get('category'),
            image_preview = data.get('image_preview'),
            article_path = data.get('article_path'),
        )

        db.add(article)
        db.commit()
    except:
        print(sys.exc_info()[0])

        # rollback the lastest commit to prevent the database connection remaining in a pending state
        db.rollback()
        return jsonify(message = 'Create article failed'), 500

@bp.route('/signup', methods=['POST'])
def signup():
    # get the JSON data from the request
    data = request.get_json()
    db = get_db()

    # create a new user using the credentials provided by the client
    try:
        user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = data.get('password')
        )

        # add it and commit to the database
        db.add(user)
        db.commit()
    except:
        # will either print:
            # 'AssertionError'
                # validation failure
            # 'sqlalchemy.exc.IntegrityError'
                # MySQL error (i.e UNIQUE constraint failure)
        print(sys.exc_info()[0])

        # rollback the lastest commit to prevent the database connection remaining in a pending state
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

    # clear the current session object
    # set the user_id and the loggedIn property of the session object to user.id and True
    # reminder that the session object from Flask and SQLAlchemy do different things
        # The SQLAlchemy version allows us to connect to the database so we can perform CRUD operations
        # The Flask version is an object that persists across requests and contains client-side data specific for the current user
    session.clear()
    session['user_id'] = user.id
    session['isAdmin'] = user.isAdmin
    session['loggedIn'] = True

    # return the user input in JSON if the request was successful
    return {
            'username': user.username,
            'email': user.email,
            'password': user.password
    }

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    # if the user is already logged in, return a JSON message instead
    if session.get('loggedIn') == True:
        return jsonify(message = 'User is already authenticated.'), 400

    try:
        # find a user with an email provided by the client
        user = db.query(User).filter(
            User.email == data['email']
        ).one()

        # verify the password for the user
        if user.verify_password(data.get('password')) == False:
            # if it's invalid, return a 400 error
            return jsonify(message = 'Incorrect credentials'), 400
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Incorrect credentials'), 400
    
    session.clear()
    session['user_id'] = user.id
    session['isAdmin'] = user.isAdmin
    session['loggedIn'] = True

    # return the user input in JSON if the request was successful
    return {
            'username': user.username,
            'email': user.email,
            'password': user.password
    }

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify(message = 'Logout successful!'), 200