from django.db import models
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, Document, IntField, StringField,DateTimeField, ListField, DictField

# class order(EmbeddedDocument):
#     order_time = DateTimeField()
#     note = StringField()

class MemberInfo(Document):
    phone = StringField(required=True, max_length=11)
    balance = IntField()
    first_order = DateTimeField()
    # recent_order = ListField(EmbeddedDocumentField(order))
    recent_order = ListField(DictField())

    meta = {
        'collection': 'members',
    }

class AuthUser(Document):
    name = StringField(required=True)
    password = StringField(required=True)

    meta = {
        'collection': 'auth',
    }
