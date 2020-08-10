from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Accomplishment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.jobTitle + ': ' + str(self.date))
    
    def get_absolute_url(self):
        return reverse('accomplishment-detail', kwargs={'pk': self.pk})