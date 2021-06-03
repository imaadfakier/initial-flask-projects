from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr___(self):
        return 'Blog post ' + str(self.id)

# all_posts = [
#     {
#         'title':'Post 1',
#         'content':'This is the content of Post 1. LAlalalala',
#         'author': 'Imaad'
#     },
#     {
#         'title':'Post 2',
#         'content':'This is the content of Post 2. LAlalalala'
#     }
# ]

@app.route('/')
def index():
    # return "<h1>Home Page</h1>"
    # return '''
    # <h1>Home Page</h1>
    # '''
    return render_template('index.html') # <- rendering html file

# NOTE: if no methods are stated, GET is only allowed by default
@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        # new_post = BlogPost(title=post_title, content=post_content, author='Imaad')
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('/posts.html', posts=all_posts)
    # return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

# @app.route('/')
# @app.route('/home')
# @app.route('/home/<string:name>') <- routing with
# @app.route('/home/<int:id>') variables
@app.route('/home/users/<string:name>/posts/<int:id>') # also known as a dynamic url
# def hello():
def hello(name, id):
    # return "Hello World"
    # return "Hello World 2"
    # return "Hello, " + str(id)
    return f"Hello, {name}, your id is: {id}"

# GET - GETting a URL
# POST - POSTing some information to a url for the given information to be saved on a database etc.
@app.route('/onlyget', methods=['GET'])
def get_req():
    return f"You can only get this webpage."

if __name__ == '__main__':
    app.run(debug=True)
