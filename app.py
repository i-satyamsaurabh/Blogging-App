from flask import Flask,request, render_template, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from datetime import datetime

from flask_migrate import Migrate




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db=SQLAlchemy(app)

migrate = Migrate(app, db)

class database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), nullable=False, unique=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)
    Content = db.Column(db.Text, nullable=False)
    Author = db.Column(db.String(20), nullable=False)
    likes = db.Column(db.Integer, default=0)
    Image = db.Column(db.String(100), nullable=True)  # New column for image filename

    def __repr__(self) -> str:
        return f"<Database {self.Title} - {self.Date}>"


    

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        Title = request.form['title']
        Content = request.form['content']
        Author = request.form['author']

        # Handle image upload
        image_file = request.files.get('imageUpload')
        image_filename = None
        if image_file:
            image_filename = image_file.filename
            image_file.save(f'static/uploads/{image_filename}')
        
        post = database(Title=Title, Content=Content, Author=Author, Image=image_filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    
    allpost = database.query.order_by(database.Date.desc()).all()
    return render_template("index.html", allpost=allpost)


@app.route("/post", methods=['GET','POST'])
def post():
    return render_template("post.html", post=post)


@app.route('/option')
def option():
    return render_template ("option.html", post=post)

@app.route('/about')
def about():
    return render_template ("About.html")


@app.route('/delete/<int:id>')
def delete(id):
    post=database.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect ('/')

@app.route('/review')
def review():
    return render_template ("review.html")

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        Title = request.form['title']
        Content = request.form['content']
        Author = request.form['author']
        post=database.query.filter_by(id=id).first()
        post.Title=Title
        post.Content=Content
        post.Author=Author
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    post=database.query.filter_by(id=id).first()
    return render_template ("update.html", post=post)



@app.route('/like/<int:id>', methods=['POST','GET'])
def like(id):
    post = database.query.filter_by(id=id).first()
    post.likes += 1
    db.session.commit()
    post=database.query.filter_by(id=id).first()
    return redirect ('/')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True, port=5000)