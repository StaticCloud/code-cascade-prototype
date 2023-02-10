from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    # references the article, only not null if the comment is top-level
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=True)
    # references parent comment, only not null if the current comment is a reply to a comment or a reply to a reply
    parent_comment = Column(Integer, ForeignKey('comments.id'), nullable=True)
    # content of comment
    comment_text = Column(String(255), nullable=False)
    # references author id
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship('User', cascade='all,delete')
    replies = relationship('Comment', remote_side=[parent_comment], cascade='all,delete')