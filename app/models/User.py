from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    isAdmin = Column(Boolean, default=False, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(50), nullable=False)

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