from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey

class Save(Base):
    __tablename__ = 'saves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))