from flask_mongoengine import Document
from mongoengine import StringField, EmailField, ListField, BooleanField, EmbeddedDocumentListField, UUIDField


class User(Document):

    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    followers = ListField(UUIDField())
    following = ListField(UUIDField())
    posts = ListField(UUIDField())
    meta = {'collection': 'users'}
