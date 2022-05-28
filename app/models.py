from datetime import datetime

from marshmallow_sqlalchemy import auto_field
from sqlalchemy import ForeignKey
from app import db
from sqlalchemy.dialects.sqlite import TEXT
from app import ma

document_tag = db.Table('documnet_tag',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(600))
    body = db.Column(db.TEXT())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=document_tag, backref='docs')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(200))

class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    tags = ma.Nested(TagSchema, many=True)
    class Meta:
        model = Document
        load_instance = True

db.create_all()
