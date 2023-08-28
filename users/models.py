from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings
from PIL import Image
import os



GENDER_CHOICE = [
    ('m', 'Male'),
    ('f', 'Female'),
]

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, birth_date, password, **other_fields):
        if not email:
            raise ValueError('You must provide an Email Address')
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")
        if not birth_date:
            raise ValueError("User must have a date of birth")
        email = self.normalize_email(email)
        user = self.model(
                    email=email, username=username,
                    birth_date=birth_date, **other_fields
                    )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, username, birth_date, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)


        if not other_fields.get('is_active'):
            raise ValueError("SuperUser must have assigned is_active=True")
        if not other_fields.get('is_staff'):
            raise ValueError("SuperUser must have assigned is_staff=True")
        if not other_fields.get('is_superuser'):
            raise ValueError("SuperUser must have assigned is_superuser=True")
        
        user = self.create_user(email, username, birth_date, password, **other_fields)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True)
    created_since = models.DateTimeField(default=timezone.now, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    # Male or Female etc
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True, blank=True)
    # Is moderator
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'birth_date']


    def __str__(self) -> str:
        return str(self.username)

    @property
    def profile_picture(self):
        return os.path.join(settings.MEDIA_URL, self.profile.image.url)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                            related_name='profile')
    image = models.ImageField(default='default_profile_picture.jpg',
                                upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Convert high resolution images to low resolution thumbnails
        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
