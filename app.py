from flask import Flask, render_template, request #render_template will return the html page in return.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


local_server = True
with open('config.json','r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)




class Contact(db.Model):
    '''
    sno, name, Email, Phone_num, msg, date 
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=True)

class Post(db.Model):
    '''
    sno, title, content, date, slug 
    '''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    img_file = db.Column(db.String(80), nullable=False)
    tag_line = db.Column(db.String(50), nullable=False)

@app.route("/")
def home():
    posts = Post.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html', params = params, posts= posts)

@app.route("/about")
def about():
    return render_template('about.html',params = params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        ''' Add entry to the database '''
        name = request.form.get('name')
        email = request.form.get('Email')
        phone_num= request.form.get('phone_num')
        Message = request.form.get('Message')

        entry = Contact(name = name, Email=email, phone_num=phone_num, date= datetime.now(), msg = Message)

        db.session.add(entry) # Add values to the session
        db.session.commit()   # Session value commmited to the database

    return render_template('contact.html',params = params)

@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):

    post = Post.query.filter_by(slug=post_slug).first()

    return render_template('post.html',params = params, post= post)

if __name__ == "__main__":
    app.run(debug = True)