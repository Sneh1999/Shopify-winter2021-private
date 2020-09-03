from datetime import datetime
from config import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


permissions = db.Table('permissions',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('image_id', db.Integer, db.ForeignKey('images.id')))

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.deferred(db.Column(db.String(100)))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    images = db.relationship(
        "Images",
        secondary = "permissions",
        backref="user",
        lazy="joined",

    )


class UserSchema(ModelSchema):
    images = fields.Nested("ImageSchema",  many=True)
    class Meta:
        model = User
        sqla_session = db.session


class ImageSchema(ModelSchema):
    
    class Meta:
        model = Images
        sqla_session = db.session

# TODO : convert and run on from http to https
# TODO : add  cascade delete 
# TODO : check if whatever thats returned from openapi3 is valid
# TODO:  check that only valid files get added
# TODO: Ensure you  keep the secret  keys somewhere
# TODO: Add definitions



