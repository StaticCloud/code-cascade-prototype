from datetime import datetime
from app.db import Base
from .Like import Like
from .Save import Save
from sqlalchemy import Column, Integer, String, DateTime, select, func, desc
from sqlalchemy.orm import relationship, column_property

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    image_preview = Column(String(255), nullable=False)
    article_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    replies = relationship("Comment", cascade='all,delete', order_by='Comment.created_at')
    likes = relationship("Like", cascade='all,delete', back_populates="article")
    saves = relationship("Save", cascade='all,delete', back_populates="article")

    like_count = column_property(
        # returns a count of rows where the article_id is equal to that of the id
        select([func.count(Like.id)]).where(Like.article_id == id)
    )

    save_count = column_property(
        # returns a count of rows where the article_id is equal to that of the id
        select([func.count(Save.id)]).where(Save.article_id == id)
    )