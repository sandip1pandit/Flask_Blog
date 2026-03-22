from datetime import datetime
import json
from flask import Flask , render_template, request ,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import flash
import os
import math
import werkzeug
from werkzeug.utils import secure_filename
local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key'#is used in Flask to securely sign session data and other security-related tokens. 
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri'] #“Connect my Flask app to the local database.”
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    ph_no = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120))
    msg = db.Column(db.String(120), nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(12), nullable=True)
    tags = db.Column(db.String(120), nullable=True)

@app.route("/")
def index():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*2 : (page-1)*2 + 2]
    if(page  == 1):
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif(page == last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts,prev=prev, next=next,last=last, page=page)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, ph_no=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
        subject="New message from " + name,
        sender=email,
        recipients=[params['gmail-user']],
        body="Name: " + name + "\nEmail: " + email + "\nPhone: " + phone + "\nMessage: " + message
)
    return render_template('contact.html', params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def login():

    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == "POST":
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if username == params['admin_user'] and userpass == params['admin_password']:
            session['user'] = username   # store session
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

        else:
            flash("Invalid credentials, Please try again! ❌", "error")
            return render_template('login.html', params=params)

    return render_template('login.html', params=params)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    # Convert sno to integer; if conversion fails, default to 0 (or handle error)
    try:
        sno = int(sno)
    except ValueError:
        # If sno is not a valid integer, treat as new post? Or abort.
        sno = 0

    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            file = request.files.get('img_file')
            file = request.files.get('img_file')

            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None
            if sno == 0:   # Create new post
                post = Posts(
                    title=box_title,
                    slug=slug,
                    content=content,
                    tags=tagline,
                    img_file=filename,
                    date=datetime.now()
                )
                db.session.add(post)
                db.session.commit()
                return redirect('/dashboard')
            else:          # Update existing post
                post = Posts.query.filter_by(sno=sno).first()
                if post is None:
                    # Handle case where post doesn't exist (e.g., redirect to dashboard)
                    return redirect('/dashboard')
                post.title = box_title
                post.slug = slug
                post.content = content
                post.tags = tagline
                if filename:
                    post.img_file = filename
                post.date = datetime.now()
                db.session.commit()
                return redirect(f'/edit/{sno}')   # Redirect back to edit form
        flash("Post Updated Successfully!", "success") 
        # GET request – render form
        post = Posts.query.filter_by(sno=sno).first() if sno != 0 else None
        return render_template('edit.html', params=params, post=post)
    
@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')
@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("You have been logged out", "success")
    return redirect('/')    
"""@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file']
            if f.filename == '':
                flash("No file selected ❌", "error")
                return redirect('/dashboard')
            else:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return redirect('/dashboard')    
"""
app.run() 