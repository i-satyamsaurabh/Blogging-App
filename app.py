from flask import Flask,request, render_template, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db=SQLAlchemy(app)


class database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), nullable=False, unique=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)
    Content = db.Column(db.Text, nullable=False)
    Author = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<database {self.Title} - {self.Date}>"

    

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        Title = request.form['title']
        Content = request.form['content']
        Author = request.form['author']
        post = database(Title=Title, Content=Content, Author=Author)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    
    allpost = database.query.order_by(desc(database.Date)).all()
    return render_template("index.html", allpost=allpost,)


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
    del_post=database.query.filter_by(id=id).first()
    if del_post:
        db.session.delete(del_post)
        db.session.commit()
    return redirect ('/')





if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True, port=5000)