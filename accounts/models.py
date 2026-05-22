from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    is_user = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('head', 'Head'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# class ProfileData(models.Model):
#     user=models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
#     profile_picture=models.ImageField(upload_to="profile_picture")
#     bio=models.TextField()
#     dob=models.DateField(null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


