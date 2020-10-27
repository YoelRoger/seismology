from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException


def sendMail(addressee, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[addressee])
    try:
        msg.body = render_template(template + '.txt', **kwargs)
        # msg.html = render_template(template + '.html', **kwargs)
        result = mailsender.send(msg)
    except SMTPException as e:
        print("ERROR OCURRIDO AL ENVIAR MAIL", str(e))
        return "MAIL DELIVER FAILED"
    return True
