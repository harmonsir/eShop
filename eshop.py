#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

import redis
from flask import Flask, render_template, request, Markup, make_response

from model import *

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
r_pipe = Redis.pipeline()
app = Flask(__name__)
Set = defaultdict(dict)


@app.route('/')
def eshop_index():
    return render_template("core-eshop.html", settings=Set)


@app.route('/c/<name>')
def pg_category(name):
    goods = Goods.query.filter_by(category_id=Markup(name))
    return render_template("core-pg-categorylist.html", settings=Set, goods=goods)


@app.route('/detail/<name>.html')
def pg_detail(name):
    good = Goods.query.filter_by(gid=Markup(name))
    return render_template("core-pg-productdetail.html", settings=Set, good=good)


@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        if request.values.get("submit") == "setting":
            Set.update(dict(request.values.items()))

        elif request.values.get("submit") == "category":
            data = req2obj_dict(request)
            for cid, dict_data in data.iteritems():
                o = Category.query.get(cid)
                for k, v in dict_data.items():
                    setattr(o, k, v)
                o.save()

                del cid, dict_data

        elif request.values.get("submit") == "goods":
            gds = Goods(**request.values.to_dict())
            gds.save()

    return render_template("core-settings.html", settings=Set)


@app.route("/robots.txt")
def robots_txt():
    response = make_response(render_template("robots.txt"))
    response.headers["Content-type"] = "text/plain; charset=utf-8"
    return response


def req2obj_dict(req):
    req = req.values.to_dict()
    tmp = defaultdict(dict)
    for k, v in req.items():
        try:
            k, idx = k.split(":")
            tmp[idx][k] = v
        except ValueError:
            pass

    return tmp


if __name__ == '__main__':
    test = dict(
        carousel_img1="/static/images/homeslide/slide-1.png",
        carousel_img2="/static/images/homeslide/slide-2.png",
        carousel_img3="/static/images/homeslide/slide-3.png",
        carousel_img4="/static/images/homeslide/slide-4.jpg",

        category1_items=Category.query.filter_by(parent_id=1),
        category2_items=Category.query.filter_by(parent_id=2),
        hot_sell_num=20,

        good_add=Goods.__table__.columns.keys()
    )
    Set.update(test)
    app.run()
