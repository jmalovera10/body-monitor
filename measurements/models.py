from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Measurement(models.Model):
    weight = models.FloatField()
    fat_percentage = models.FloatField()
    muscle_percentage = models.FloatField()
    calories = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    