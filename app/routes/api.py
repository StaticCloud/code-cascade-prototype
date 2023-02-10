import json
from flask import Blueprint, request, jsonify, session, render_template
from app.models import Comment, Article
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

    articles = db.query(Article).filter(Article.id == id).order_by(Article.created_at.desc()).all()

    return {
        'articles': [
            {
                'author': article.author.username,
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
            for article in articles
        ]
    }
