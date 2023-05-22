from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Save(Base):
    __tablename__ = 'saves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))

    article = relationship('Article', back_populates="saves", cascade='all,delete')