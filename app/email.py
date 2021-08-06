from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_notification(name,receiver):
    # Creating message subject and sender
    subject = 'Alumni'
    sender = 'bernard.kibet@student.moringaschool.com'

    #passing in the context vairables
    text_content = render_to_string('email/newsemail.txt',{"name": name})
    html_content = render_to_string('email/newsemail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()