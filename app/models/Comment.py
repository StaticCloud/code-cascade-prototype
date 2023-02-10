from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    replies = relationship('Reply', cascade='all,delete')