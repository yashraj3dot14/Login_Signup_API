from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#for sending mail
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned with is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned with is_superuser=True')

        return self.create_user(email, first_name, password, **other_fields)


    def create_user(self, email, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide meial address'))

        email = self.normalize_email(email) #convert into lowercase
        user = self.model(email= email, first_name= first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    #username = None
    email = models.EmailField(_('Email address'), unique= True)
    first_name = models.CharField(max_length= 150, blank= True)
    last_name = models.CharField(max_length= 150, blank= True)
    mobile = models.CharField(max_length= 12)
    start_date = models.DateTimeField(default= timezone.now())
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= False)

    objects = CustomAccountManager() #tells Django that we are using custom user model,add in AUTH_USER_MODEL insettings.py
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email


#for password reset
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="ABC.com password reset"),
        # message:
        email_plaintext_message,
        # from:
        "djangotesting97@gmail.com",
        # to:
        [reset_password_token.user.email]
    )