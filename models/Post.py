from mongoengine import StringField, ListField, UUIDField, Document
import uuid


class Post(Document):
    ID = UUIDField(primary_key=True, default=uuid.uuid4)
    originalPostBy = StringField(required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    qtype = StringField(default='Global')
    code = StringField(required=True)
    testcases = ListField(StringField(), required=True)
    outputs = ListField(StringField(), required=True)
    solvedBy = ListField(StringField())
    meta = {'collection': 'posts'}
