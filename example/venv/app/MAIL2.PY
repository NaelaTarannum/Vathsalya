from flask import Flask,request
from flask_mail import Mail,Message
app=Flask(__name__)
app.config['MAIL_SERVER']='imap.gmail.com'
app.config['MAIL_PORT']=993
app.config['MAIL_USE_SSL']=True
app.config.from_pyfile('config.cfg')

mail=Mail(app)

@app.route('/',methods=['GET','POST'])
def index():
    msg=Message('Hello',sender='rushika1997@gmail.com',recipients=['naela16@gmail.com'])
    mail.send(msg)
    return 'mail sent!'



if __name__=='__main__':
    app.run(debug=True)
