import json
from flask import Blueprint, request, jsonify, session, render_template
from app.models import Comment, Reply
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

def getAllReplies(parent_reply):
    
    replies = [];

    if parent_reply.replies:
        for reply in parent_reply.replies:

            nested_replies = getAllReplies(reply)

            replies.append({
                "id": reply.id,
                "comment_text": reply.comment_text,
                "replies": nested_replies
            })

    return replies




@bp.route('/comments', methods=['GET'])
def comments():
    db = get_db()

    # query comments
    comments = db.query(Comment).order_by(Comment.created_at.desc()).all()
    
    return {
        # return data formatted as JSON object
        'data': [
            {
                # return comment text and replies for top-level comments
                'comment_text': comment.comment_text,
                'replies': [
                    {
                        # return the id, comment text, and nested replies for each reply
                        "id": reply.id,
                        "comment_text": reply.comment_text,
                        "replies": getAllReplies(reply) # recursive function to iterate through nested replies
                    }
                    for reply in comment.replies # iterate through comment replies
                ]
            }
            for comment in comments # iterate through all top level comments
        ]
    }
