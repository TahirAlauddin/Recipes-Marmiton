from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed, user_signed_up
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

User = get_user_model()
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(email_confirmed, sender=User)
def activate_user(sender, request, email_address, **kwargs):
    email_address = EmailAddress.objects.get(email=email_address.email)
    user = User.objects.get(email=email_address)
    user.is_confirmed = True
    user.save()
