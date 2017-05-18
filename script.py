#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
r_pipe = Redis.pipeline()

settings = [
    ("index:carousel", dict(
        img1="/static/images/homeslide/slide-1.png",
        img2="/static/images/homeslide/slide-2.png",
        img3="/static/images/homeslide/slide-3.png",
        img4="/static/images/homeslide/slide-4.jpg",
    )),
    ("index:hot.sell", dict(
        number=20,
        items=[]
    )),
    ("index:feature", dict(
        items=[]
    )),

    ("eshop:category", dict(
        c1=["Newest", "Hottest", "Concessional"],
        c2=["Mobile Battery", "Case Battery", "Protection class", "Power Bank"],
    )),

    ("eshop:category:c2:1", dict(title="Case Battery", img="/static/images/forwomens.jpg", link=1),),
    ("eshop:category:c2:2", dict(title="Case Battery", img="/static/images/forwomens.jpg", link=1),),
    ("eshop:category:c2:3", dict(title="Protection class", img="/static/images/footwear.jpg", link=1),),
    ("eshop:category:c2:4", dict(title="Power Bank", img="/static/images/accessoriess.png", link=1),),

    ("eshop:goods:[cid]:[gid]", dict()),
]

for k, v in settings:
    r_pipe.hmset(k, v)
r_pipe.execute()

print Redis.hgetall("index:carousel")
