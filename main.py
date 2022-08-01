# Main python code for Mass Mail Dispatcher

from flask import Flask , render_template, request
#Flask is the prototype used to create instances of web application 
#render_template : Renders a template from the template folder with the given context
# request : to collect data from client's web page


from flask_mail import Mail, Message
# Mail : manage email messages
# Message : Encapsulates an email message.


from validate_email import validate_email            
# to check if an email id is valid and if it exists

import csv          # to manage csv files

import DNS
DNS.defaults['server']=['8.8.8.8', '8.8.4.4']


app=Flask(__name__)                                   # takes the name of current module (__name__) as argument
@app.route("/")                                       # route() : is a decorator, which tells the application which URL should call the associated function
def confirm():
    return (render_template("home.html"))             #takes to the home page


#passing the value from the form filled on home page
@app.route("/verify",methods=['POST','GET'])

def home():
    
    
    if request.method=='POST':

        global attach    # made global to use it in verification page
        
        email=request.form['mail']
        password=request.form['pass']
        subject=request.form['sub']
        body=request.form['msg']
        recip=request.form['file']
        attach=request.form.getlist('attach')
        
        
        #opening the recipients files
        with open(recip) as f:
            reader=csv.reader(f)
            next(reader)
            result1=[]           #collection for valid mails
            result2=[]           #collection for invalid mails

            #creating the valid recipients files
            with open("valid.csv",'w') as f1:
                writer=csv.writer(f1)
                for f in reader:
                    is_valid = validate_email(f[0], check_mx=True, verify=True)          #check if the recipient's email-id is valid or not and if it exists
                    if (is_valid==False):
                        result2.append(f[0])
                        pass
                    else:
                        result1.append(f[0])
                        writer.writerow(f)

        return render_template("confirm.html", invalid=result2, valid=result1, mls=email, pas=password, sb=subject, bd=body)


@app.route("/send", methods=['POST','GET'])
def send():
    email=request.form['mail']
    password=request.form['pass']
    app.config['MAIL_SERVER']='smtp.gmail.com'               #server for sending mails
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']=email
    app.config['MAIL_PASSWORD']=password                                                   #'weznrnljngxxklqc'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True
    mail=Mail(app)
    if request.method=='POST':


        subject=request.form['sub']
        body=request.form['msg']
        recip="valid.csv"
        
        count=0
        with open(recip) as f:
            reader=csv.reader(f)
            for f in reader:
                try:
                    msg=Message(subject,sender=email, recipients=[f[0]])
                    for file in attach:
                        try:
                            with app.open_resource(file) as fp:
                                msg.attach(file, "application/octet-stream", fp.read())     # here you need to attach any attachment
                        except:
                            pass
                    msg.body=body
                    mail.send(msg)                        # sending the mail
                    count+=1
                except:
                    pass
        return render_template("result.html",cnt=count)

            



@app.route("/home")
def back():
    return render_template("home.html")


if __name__== '__main__':
    app.run(debug=True)