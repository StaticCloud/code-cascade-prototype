from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Reply(Base):
    __tablename__ = 'replies'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    parent_comment = Column(Integer, ForeignKey('comments.id'), nullable=True)
    parent_reply = Column(Integer, ForeignKey('replies.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    replies = relationship("Reply", remote_side=[parent_reply], cascade='all,delete')