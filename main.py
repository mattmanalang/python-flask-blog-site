from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, TelField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Optional
import requests
import smtplib
import os


class ContactForm(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired()], render_kw={"placeholder": "Enter your name..."})
    email = StringField(label="Email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Enter your email..."})
    phone = TelField(label="Telephone", validators=[Optional()], render_kw={"placeholder": "Enter your phone number..."})
    message = TextAreaField(label="Message", validators=[InputRequired()], render_kw={
        "placeholder": "Enter your message...",
        "style": "height: 12rem"
    })
    send = SubmitField(label="Send")


def send_email(message_data):
    user = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=user, password=password)
        connection.sendmail(from_addr=user,
                            to_addrs=os.getenv('RECIPIENT_EMAIL'),
                            msg=f"Subject:New Message From The Blog Site!\n\n"
                                f"Name: {message_data['name']}\n"
                                f"Email: {message_data['email']}\n"
                                f"Phone: {message_data['phone']}\n"
                                f"Message: {message_data['message']}")


app = Flask(__name__)
app.secret_key = "thisisntarealkey"
bootstrap = Bootstrap5(app)
blog_data_url = "https://api.npoint.io/cdc3fdc6b1d7e604581a"
blog_data = requests.get(blog_data_url).json()
indexed_posts = {post['id']: post for post in blog_data}


@app.route("/")
def home():
    return render_template("index.html", posts=indexed_posts.values())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        send_email(request.form)
        return render_template("contact.html", form=contact_form, form_complete=True)
    else:
        return render_template("contact.html", form=contact_form, form_complete=False)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return render_template("post.html", post=indexed_posts[post_id])


if __name__ == "__main__":
    app.run(debug=True)
