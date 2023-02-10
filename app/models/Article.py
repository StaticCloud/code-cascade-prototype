from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    image_preview = Column(String(255), nullable=False)
    article_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship('User')
    replies = relationship("Comment", cascade='all,delete')
    likes = relationship("Like", cascade='all,delete')