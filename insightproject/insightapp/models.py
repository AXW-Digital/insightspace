from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import random
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail  

# Create your models here.

#Usermanager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError('Email address is required for this action')
        if not password:
            raise ValueError('Password is required')

        user_obj = self.model(email=email)

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email,password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_admin=True)
        return user





#user model
class User(AbstractBaseUser):
    """model for abstract user"""
    email = models.EmailField(max_length=50, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        if self.fname:
            return self.fname
        else:
            return self.email

    def get_last_name(self):
        if self.lname:
            return self.lname
        else:
            return self.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



    
def upload_image_path_profile(instance, filename):
    """method helps in image uploading as profile image"""
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    """helper method for image path"""
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext



class Profile(models.Model):
    """model for a user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_profile, default=None, blank = True, null=True)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Numero muodossa: '+3581234567890'.")
    phone = models.CharField(validators=[phone_regex], max_length=16, blank=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    post_regex = RegexValidator(regex=r'^(^[0-9]{5}(?:-[0-9]{4})?$|^$)', message='Length mus be 5', code='nomatch')
    post_number = models.CharField(max_length=5, validators=[post_regex], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


def user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
post_save.connect(user_create_reciever, sender=User)


#password reset: dropping this one not in use requires 
""""@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )"""

#asiointi kysely
class Asiointi(models.Model):
    yksi = models.CharField(max_length=100)
    kaksi = models.CharField(max_length=100)
    kolme = models.CharField(max_length=100)
    nelja = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="asiointis", on_delete=models.CASCADE, null=True)

#ruokalista kysely
class Ruokalista(models.Model):
    viisi = models.CharField(max_length=100)
    kuusi = models.CharField(max_length=100)
    seitseman = models.CharField(max_length=100)
    kahdeksan = models.CharField(max_length=100)
    yhdeksan = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="ruokalistas", on_delete=models.CASCADE, null=True)


#mika vaikuttaa ravintolan valintaan
class RavinVaikutu(models.Model):
    kymenen = models.CharField(max_length=100)
    yksitoista = models.CharField(max_length=100)
    kaksitoista = models.CharField(max_length=100)
    kolmetoista = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="ravinvaikutus", on_delete=models.CASCADE, null=True)


#perustiedot
class Perustiedot(models.Model):
    yksi = models.CharField(max_length=100)
    kaksi = models.CharField(max_length=100)
    kolme = models.CharField(max_length=100)
    nelja = models.CharField(max_length=100)
    viisi = models.CharField(max_length=100)
    kuusi = models.CharField(max_length=100)
    seitseman = models.CharField(max_length=100)
    kahdeksan = models.CharField(max_length=100)
    yhdeksan = models.CharField(max_length=100)
    kymenen = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="perustiedots", on_delete=models.CASCADE, null=True)