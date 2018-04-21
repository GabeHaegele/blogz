from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secrecy1'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    text = db.Column(db.Text())

    def __init__(self, name, text):
        self.name = name
        self.text = text

@app.route('/', methods=['POST', 'GET'])
def index():   
    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        blog=Blog.query.get(blog_id)
        return render_template('sing-blog.html', blog=blog)
    blogs = Blog.query.all()
    return render_template('blogs.html',title="My Posts!",blogs=blogs)
     
@app.route('/add-blog', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_body = request.form['text']
        if not blog_name or not blog_body:
            flash("Title and body text required")
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/?id='+str(new_blog.id))
    return render_template('new-post.html')
    


if __name__ == '__main__':
    app.run()

"""
python
from main import db, Blog
db.create_all()
db.session.commit()
"""