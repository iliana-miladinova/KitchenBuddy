from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    GENDER = [ ('Male', 'Male'), ('Female', 'Female')]

    ACTIVITY = (('sedentary', 'sedentary'), ('light', 'light active'),
                ('moderate', 'moderate active'), ('very', 'very active'))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    activity = models.CharField(max_length=20, choices=ACTIVITY, blank=True)
    calories = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"This is {self.user.username}'s Profile"