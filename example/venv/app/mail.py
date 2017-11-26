import smtplib
from flask import Flask,request
server = smtplib.SMTP('smtp.gmail.com',587)
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'GET':
       return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

server.starttls()

mail=request.form['email']
user_email ='rushika1997@gmail.com'

user_password=' blue2335'

target_email=mail

server.login(user_email,user_password)

server.sendmail(user_email,target_email,"hello")
