import sys
from flask import Blueprint, request, jsonify, session
from sqlalchemy import and_, extract
from app.models import Comment, Article, User, Like, Save
from app.utils.auth import login_required
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

def getAllReplies(parent_reply, depth):
    replies = [];
    if parent_reply.replies:
        for reply in parent_reply.replies:

            nested_replies = getAllReplies(reply, depth)

            replies.append({
                "id": reply.id,
                "author": reply.author.username,
                "comment_text": reply.comment_text,
                "replies": nested_replies,
                "total_replies": getReplyCount(reply),
                'depth': depth + 1
            })

    return replies

def getReplyCount(comment):
    total = 0;
    if comment.replies:
        for reply in comment.replies:
            total += 1 + getReplyCount(reply)
    return total;


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
                'depth': 0,
                'comment_text': comment.comment_text,
                'replies': [
                    {
                        # return the id, comment text, and nested replies for each reply
                        "id": reply.id,
                        "comment_text": reply.comment_text,
                        "replies": getAllReplies(reply, 1), # recursive function to iterate through nested replies
                        'total_replies': getReplyCount(reply),
                        'depth': 1
                    }
                    for reply in comment.replies # iterate through comment replies
                ],
                'total_replies': getReplyCount(comment)
            }
            for comment in comments # iterate through all top level comments
        ]
    }

@bp.route('/comment', methods=['POST'])
def comment():
    data = request.get_json()
    db = get_db()

    try:
        comment = Comment(
            article_id=data.get('article_id'),
            comment_text=data.get('comment_text'),
            author_id=session.get('user_id')
        )

        db.add(comment)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Create comment failed'), 500
    
    return '', 204

@bp.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    db = get_db()

    try:
        reply = Comment(
            parent_comment=data.get('parent_comment'),
            comment_text=data.get('comment_text'),
            author_id=session.get('user_id')
        )

        db.add(reply)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Create reply failed'), 500
    
    return '', 204

@bp.route('/article/<id>', methods=['GET'])
def articles(id):
    db = get_db()
    article = db.query(Article).filter(Article.id == id).order_by(Article.created_at.desc()).one()
    return {
            'title': article.title,
            'category': article.category,
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

        db.rollback()
        return jsonify(message = 'Create article failed'), 500
    
    return {
            'id': article.id,
            'title': article.title,
            'category': article.category
    }

@bp.route('/editProfile', methods=['PUT'])
@login_required
def updateUser():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.id == session.get('user_id')).one()
        
        user.bio = data.get('bio')
        user.linkedin = data.get('linkedin')
        user.github = data.get('github')
        user.avatar = data.get('avatar')

        session['avatar'] = user.avatar

        db.commit();
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'User not found'), 404
    
    return '', 204


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
            password = data.get('password'),
            avatar = '/img/avatar_8.png'
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
    session['avatar'] = user.avatar

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
    session['avatar'] = user.avatar

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

@bp.route('/search', methods=['GET'])
def search():
    db = get_db()
    args = request.args.to_dict();

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

    return [{
        'category': article.category,
        'created_at': article.created_at,
        'title': article.title,
        'like_count': article.like_count,
        'save_count': article.save_count
    } for article in articles];


@bp.route('/article/like', methods=['POST'])
@login_required
def like():
    data = request.get_json()
    db = get_db()

    try:
        like = Like(
            user_id = session.get('user_id'),
            article_id = data.get('article_id')
        )

        db.add(like)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Failed to add like'), 500

    return '', 200

@bp.route('/article/removeLike', methods=['DELETE'])
@login_required
def removeLike():
    data = request.get_json()
    db = get_db()

    try:
        db.delete(db.query(Like).filter(
            and_(
                Like.article_id == data.get('article_id'),
                Like.user_id == session.get('user_id')
            )).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Failed to remove like'), 404

    return '', 200

@bp.route('/article/save', methods=['POST'])
@login_required
def save():
    data = request.get_json()
    db = get_db()

    try:
        save = Save(
            user_id = session.get('user_id'),
            article_id = data.get('article_id')
        )

        db.add(save)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Failed to save article'), 500

    return '', 200

@bp.route('/article/unsave', methods=['DELETE'])
@login_required
def unsave():
    data = request.get_json()
    db = get_db()

    try:
        db.delete(db.query(Save).filter(
            and_(
                Save.article_id == data.get('article_id'),
                Save.user_id == session.get('user_id')
            )).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Failed to unsave article'), 404

    return '', 200