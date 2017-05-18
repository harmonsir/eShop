#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

from __init__ import app

db = SQLAlchemy(app)


class BaseFunc(object):
    def row2dict(self, r):
        return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def save(self):
        db.session.add(self)
        db.session.commit()


class Section(db.Model, BaseFunc):
    sid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Section %r>" % self.username


class Category(db.Model, BaseFunc):
    cid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    img = db.Column(db.BINARY, nullable=True)
    lv = db.Column(db.VARCHAR, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("section.sid"))
    section = db.relationship("Section", backref=db.backref("section", lazy="dynamic"))
    sort = db.Column(db.SmallInteger)
    is_feature = db.Column(db.BOOLEAN)

    def __init__(self, section=None, title="", img="", lv=2, sort=0, is_feature=0):
        if section:
            self.section = section

        self.title = title
        self.img = img
        self.lv = lv
        self.sort = sort
        self.is_feature = is_feature

    def __repr__(self):
        return "<Category %r>" % self.username


class Goods(db.Model, BaseFunc):
    gid = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.cid"))
    category = db.relationship("Category", backref=db.backref("category", lazy="dynamic"))

    title = db.Column(db.VARCHAR)
    intro = db.Column(db.VARCHAR, nullable=True)
    imgs = db.Column(db.BINARY, nullable=True)
    price = db.Column(db.SmallInteger, default=0)
    # stock = db.Column(db.SmallInteger, default=1)
    buy_link = db.Column(db.VARCHAR, nullable=True)
    description = db.Column(db.Binary, nullable=True)
    additional = db.Column(db.Binary, nullable=True)

    def __init__(self, title, intro, imgs=dict([]), *args, **kwargs):
        if kwargs.get("category"):
            self.category = kwargs["category"]

        self.title = title
        self.intro = intro
        self.imgs = imgs

    def __repr__(self):
        return "<Goods %r>" % self.username


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    s1 = Section("Event")
    s2 = Section("Products")
    for item in [s1, s2]:
        item.save()

    c1 = Category(Section.query.get(1), "Newest")
    c2 = Category(Section.query.get(1), "Hottest")
    c3 = Category(Section.query.get(1), "Concessional")
    # db.session.bulk_save_objects([c1, c2, c3])
    db.session.commit()

    c1 = Category(Section.query.get(2), "Mobile Battery", img="/static/images/hc-outerwear.jpg")
    c2 = Category(Section.query.get(2), title="Case Battery", img="/static/images/forwomens.jpg")
    c3 = Category(Section.query.get(2), title="Protection class", img="/static/images/footwear.jpg")
    c4 = Category(Section.query.get(2), title="Power Bank", img="/static/images/accessoriess.png")
    # db.session.bulk_save_objects([c1, c2, c3, c4])
    db.session.commit()
