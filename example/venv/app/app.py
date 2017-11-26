
from flask import Flask, render_template,request,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_mail import Mail, Message
from twilio.rest import Client
import pdfkit

account_sid ="AC540c810fc17d56c755bf320ec08a3fc4"
# Your Auth Token from twilio.com/console
auth_token  = "35f7efcd609c4a3a855e66fa42e60172"

client = Client(account_sid, auth_token)





engine = create_engine('sqlite:///tutorial.db', echo=True)
app = Flask(__name__)
app.config.from_object('config')
mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:nasreensultana@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['DEBUG']=True
app.config['WHOOSH_BASE']='whoosh'

db=SQLAlchemy(app)
class  Slot(db.Model):

     id=db.Column(db.Integer,primary_key=True);
     name = db.Column(db.String(30))
     number = db.Column(db.VARCHAR(15))
     date = db.Column(db.Date)
     email=db.Column(db.VARCHAR(15))
     db.create_all()

class  Post(db.Model):

     __tablename__ = 'Post'
     __searchable__ = ['id','name']
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(30))
     age= db.Column(db.VARCHAR(10))
     gender=db.Column(db.VARCHAR(1))
     school=db.Column(db.VARCHAR(10))
     height=db.Column(db.Float(5,2))
     health=db.Column(db.String(20))
     blood=db.Column(db.VARCHAR(10))
     db.create_all()

def __repr__(self):
     return '{0}(title={1})'.format(self.__class__.__name__, self.name)

wa.whoosh_index(app,Post)

@app.route('/search',methods=['GET'])

def search(Post):

     with app.test_request_context():
            from flask import request# Do Expensive work
            posts =Post.query.whoosh_search(request.args.get('query')). all()
            return render_template('records.html',posts=posts)

class Donate(db.Model):

     id=db.Column(db.Integer,primary_key=True)
     name1=db.Column(db.String(100))
     address=db.Column(db.String(100))
     amount=db.Column(db.VARCHAR(10))
     number=db.Column(db.VARCHAR(20))
     name=db.Column(db.VARCHAR(20))
     cardnum=db.Column(db.VARCHAR(50))
     expiration=db.Column(db.VARCHAR(25))
     security=db.Column(db.VARCHAR(5))




@app.route('/naela', endpoint = 'naela',methods=['GET','POST'])
def naela():
    if request.method == 'POST':
        slot = Slot(number=request.form['number'],name=request.form['name'],date=request.form['date'],email=request.form['email'])
        db.session.add(slot)
        db.session.commit()
        message = client.messages.create(
            body="Thank you for interest in Vathsalya.Your slot has been booked for"+ str(slot.date) ,
            to=slot.number,
            from_="+19032253810"
            )

        print(message.sid)

        return render_template('index3.html')


@app.route('/rida')
def rida():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        posts =Post.query.all()
        return render_template('records.html',posts=posts)
    return logout()

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return rida()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return rida()

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        post = Post(name=request.form['name'],age=request.form['age'],gender=request.form['gender'],school=request.form['school'],height=request.form['height'],health=request.form['health'],blood=request.form['blood'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('rida'))
    return render_template('add.html')


@app.route('/donate1',methods=['GET','POST'])
def donate1():
    if request.method == 'POST':
        donate=Donate(name1=request.form['name1'],address=request.form['address'],amount=request.form['amount'],number=request.form['number'],name=request.form['name'],expiration=request.form['expiration'])#,cardnum=request.form['cardnum'],security=request.form['security'])
        db.session.add(donate)
        db.session.commit()
        return redirect(url_for('pdf_template'))
    return render_template('donate1.html')

@app.route('/pdf_template/')
def pdf_template():
    voice=Donate.query.all()
    rendered = render_template('invoice.html',voice=voice)
    css=['invoicestyle.css']
    pdf = pdfkit.from_string(rendered,False,css=css)

    response=make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition']='inline filename=output.pdf'
    return response

@app.route('/')
def index3():

    return render_template('index3.html')
if __name__=='__main__':
    app.run(debug='true')
