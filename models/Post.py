from mongoengine import StringField, ListField, UUIDField
from flask_mongoengine import Document
import uuid


class Post(Document):
    ID = UUIDField(primary_key=True, default=uuid.uuid4)
    originalPostBy = StringField(required=True)
    question = StringField(required=True)
    code = StringField(required=True)
    testcases = ListField(StringField, required=True)
    outputs = ListField(StringField, required=True)
    solvedBy = ListField(StringField)
