from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='メールアドレス', unique=True)
    first_name = models.CharField(verbose_name='姓', max_length=20)
    last_name = models.CharField(verbose_name='名', max_length=20)
    telephone_number = models.CharField('電話番号', max_length=30, blank=True)
    post_code = models.CharField('郵便番号', max_length=30, blank=True)
    address = models.CharField('住所', max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_card_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

class Marker(models.Model):
    id = models.AutoField('マーカーID', primary_key=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

class Review(models.Model):
    id = models.AutoField('レビューID', primary_key=True)
    marker = models.ForeignKey(Marker, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Marker {self.marker.id}"

class TopImage(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)
    
    def __str__(self):
        return str(self.image)

class SelfIntroduction(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)
    second_image = models.ImageField(upload_to='images', verbose_name='イメージ画像', blank=True, null=True)
    
    def __str__(self):
        return str(self.image)