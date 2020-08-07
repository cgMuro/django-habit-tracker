from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Habit(models.Model):
    activity = models.CharField(max_length=100)
    time_spent = models.IntegerField(verbose_name='Time Spent (in minutes)')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField('Date of creation', default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Habit: {self.activity} for {self.time_spent}. When: {self.created_at}"