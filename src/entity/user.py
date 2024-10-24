# Libraries
from flask import current_app
from typing_extensions import Self
from werkzeug.security import generate_password_hash, check_password_hash

# Local dependencies
from .sqlalchemy import db

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), nullable=False, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    # Foreign key to the Profile model
    user_profile = db.Column(db.String(100), db.ForeignKey('profiles.name'), nullable=False)

    # Relationship with Profile model
    profile = db.relationship('Profile', backref='users')

    def set_password(self, password):
        """Hash the password before storing it."""
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Verify the password hash."""
        return check_password_hash(self.password, password)

    def to_dict(self) -> dict[Self]:
        """Return a dictionary representation of the user."""
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),
            'user_profile': self.user_profile
        }

    @classmethod
    def checkLogin(cls, email:str, password:str) -> Self:
        user = cls.queryUserAccount(email)
    
        if not user or not user.check_password(password):
            return False

        return True
    
    @classmethod
    def queryUserAccount(cls, email:str) -> Self | None:
        # Query a specific user profile based on parameter email
        # return a User object or None
        return cls.query.filter_by(email=email).one_or_none()
    
    @classmethod
    def queryAllUserAccount(cls) -> list[Self]:
        # Query all users
        # Return list of all User objects
        return cls.query.all()
    
    @classmethod
    def createUserAccount(cls, email:str, password:str = "Placeholder",
                          first_name:str = False,
                          last_name:str = False,
                          dob: bool = False,
                          user_profile:str = False):
        
        if cls.queryUserAccount(email):
            return False

        new_user = cls(
            email=email,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            user_profile=user_profile
        )

        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()

        return True

    @classmethod
    def updateUserAccount(cls, email, password, first_name, last_name, dob, user_profile):
        try:
            with current_app.app_context():
                user = cls.query.filter_by(email=email).one_or_none()
                if not user:
                    return False, 404
                
                if password is not None:
                    user.password = generate_password_hash(password)
                if first_name is not None:
                    user.first_name = first_name
                if last_name is not None:
                    user.last_name = last_name
                if dob is not None:
                    user.dob = dob
                if user_profile is not None:
                    user.user_profile = user_profile

                db.session.commit()
                return True, 200

        except Exception as e:
            db.session.rollback()
            return False, 500