from flask_mongoengine import Document
from mongoengine import StringField, EmailField, ListField


class User(Document):

    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    followers = ListField(StringField)
    following = ListField(StringField)
    posts = ListField(StringField)
