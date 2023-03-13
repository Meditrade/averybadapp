import flask
import sqlite3
import json


from flask import Flask
from flask import request

app = Flask(__name__)


@app.post("/register")
def register():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    j = json.loads(request.data)
    
    cur.execute("CREATE TABLE IF NOT EXISTS users(id int, username text, password text);")

    #Get the current latest ID 
    res = cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1;")
    id = 0 if res.fetchone() is None else res.fetchone()

    cur.execute("insert INTO users VALUES('%s','%s','%s')" % (str(id+1), j["username"], j["password"]) )
    con.commit()

    return "", 200


@app.post("/login")
def login():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    j = json.loads(request.data)
    
    cur.execute("CREATE TABLE IF NOT EXISTS users(id int, username text, password text);")


    res = cur.execute("SELECT * FROM users WHERE username='%s' AND password='%s';" % (j["username"], j["password"]))
    u = res.fetchone()
    if u is None:
        return "No such user or password incorrect!", 404
    else: 
        id = u[0]
    return '{"id": %s}' % id

@app.post("/new_blog_post")
def new_bp():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("create table if not exists blog_posts(id int, user_id int, content text)")    
    j = json.loads(request.data)

    #Get the current latest ID 
    res = cur.execute("SELECT * FROM blog_posts ORDER BY id DESC LIMIT 1;")
    fetchone = res.fetchone()[0]
    id = 0 if fetchone is None else fetchone

    cur.execute("insert into blog_posts values('%s', '%s', '%s')" % ( str(id+1), j["user_id"], j["content"]))
    con.commit()

    return "", 200

@app.get("/blog")
def blog():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("create table if not exists blog_posts(id int, user_id int, content text)")
    con.commit()

    res = cur.execute("select * from blog_posts;")
    posts = res.fetchall()


    # Todo add authors name!
    return "\n".join([post[2] for post in posts]) , 200


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"