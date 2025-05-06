from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import AlumniProfile

@receiver(post_save, sender=User)
def create_alumni_profile(sender, instance, created, **kwargs):
    """Create AlumniProfile for new users"""
    if created:
        AlumniProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_alumni_profile(sender, instance, **kwargs):
    """Save AlumniProfile when User is saved"""
    instance.alumniprofile.save()