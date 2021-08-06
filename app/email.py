from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decouple import config

def send_notification(name,receiver):
    # Creating message subject and sender
    subject = 'Alumni'
    sender = config('EMAIL_HOST_USER')

    #passing in the context vairables
    text_content = render_to_string('email/newsemail.txt',{"name": name})
    html_content = render_to_string('email/newsemail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

#function sending email to an invitee email address
def send_invite(receiver, domain , uid, token):
    subject = 'Invitation to Alumni Community'
    sender = config('EMAIL_HOST_USER')

    text_content = render_to_string('email/inviteemail.txt',{'domain':domain, 'uid':uid, 'token':token})
    html_content = render_to_string('email/inviteemail.html',{'domain':domain, 'uid':uid, 'token':token})

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#function sending email to owner of an idea to be a collaborator
def collaborate_new(new_collab, idea, receiver, skills):
    subject = 'Your idea has a new collaborator'
    sender = config('EMAIL_HOST_USER')

    text_content = render_to_string('email/collaborateemail.txt',{'idea':idea, 'skills':skills, 'new_collab':new_collab})
    html_content = render_to_string('email/collaborateemail.html',{'idea':idea,'skills':skills, 'new_collab':new_collab})

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()