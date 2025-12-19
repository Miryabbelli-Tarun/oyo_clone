import uuid
# from django.core.mail import send_mail
# from django.conf import settings

def generateRandomToken():
    return str(uuid.uuid4())

# def sendEmailToken(email,token):
    
#     message=f""" verify your account by clicking this link
#         http://127.0.0.1:8000/accounts/verify-account/{token}
#     """
#     send_mail(
#         subject="verify your email",
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False
#     )
