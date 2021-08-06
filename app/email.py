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

#function sending email to an invitee email address
def send_invite(name, receiver):
    subject = 'Invitation to Alumni Community'
    sender = 'bernard.kibet@student.moringaschool.com'

    text_content = render_to_string('email/inviteemail.txt',{'name':name})
    html_content = render_to_string('email/inviteemail.html',{'name':name})

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#function sending email to owner of an idea to be a collaborator
def collaborate_new(new_collab, name, receiver, skills):
    subject = 'Your idea has a new collaborator'
    sender = 'bernard.kibet@student.moringaschool.com'

    text_content = render_to_string('email/collaborateemail.txt',{'name':name, 'skills':skills, 'new_collab':new_collab})
    html_content = render_to_string('email/collaborateemail.html',{'name':name,'skills':skills, 'new_collab':new_collab})

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()