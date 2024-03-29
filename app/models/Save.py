from app.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Save(Base):
    __tablename__ = 'saves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))
    created_at = Column(DateTime, default=datetime.now)

    article = relationship('Article', back_populates="saves", cascade='all,delete')