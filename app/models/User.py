from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates, relationship
import bcrypt

salt = bcrypt.gensalt()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    isAdmin = Column(Boolean, default=False, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(50), default="/img/placeholder-pfp.png", nullable=False)
    bio = Column(String(250), nullable=False, default="")
    linkedin = Column(String(50), nullable=False, default="")
    github = Column(String(50), nullable=False, default="")

    liked_articles = relationship("Like", order_by='Like.created_at.desc()')
    saved_articles = relationship("Save", order_by='Save.created_at.desc()')
    comments = relationship("Comment", order_by='Comment.created_at.desc()')

    @validates('email')
    def validate_email(self, key, email):
        # ensure there is a @ character in the email
        assert '@' in email
        return email;

    @validates('password')
    def validate_password(self, key, password):
        # ensure the password is greater than 4 characters
        assert len(password) > 4

        # hash password
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password):
        # validate the password
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )