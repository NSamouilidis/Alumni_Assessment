from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class School(models.Model):
    """Model for Mediterranean College's Schools"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('alumni:school_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['name']

class AlumniProfile(models.Model):
    """Model for alumni profiles"""
    STATUS_CHOICES = (
        ('applied', 'Applied Alumni'),
        ('registered', 'Registered Alumni'),
    )
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name='alumni')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    
    # Personal Information
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Academic Information
    graduation_year = models.IntegerField(null=True, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    
    # Professional Information
    current_company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
    
    def get_absolute_url(self):
        return reverse('alumni:profile_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ['-updated_at']

class Event(models.Model):
    """Model for alumni events"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    
    # For registration
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    attendees = models.ManyToManyField(AlumniProfile, related_name='events', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('alumni:event_detail', kwargs={'pk': self.pk})
    
    @property
    def is_past_event(self):
        return self.date < timezone.now()
    
    @property
    def can_register(self):
        if not self.registration_required:
            return False
        if self.is_past_event:
            return False
        if self.registration_deadline and self.registration_deadline < timezone.now():
            return False
        return True
    
    class Meta:
        ordering = ['-date']