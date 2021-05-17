from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def mailing(username):
    email_list = []
    obj = User.objects.filter(is_superuser=True)
    for user in obj:
        email_list.append(user.email)
    subjects = 'hello'
    body = f'User with {username} register in military database, please check him!'
    email = EmailMessage(subject=subjects, body=body, to=email_list)
    email.send()


def validate_password(password):
    if len(password) >= 8 and not password.isdigit() and not password.isalpha():
        return True
    else:
        return False
