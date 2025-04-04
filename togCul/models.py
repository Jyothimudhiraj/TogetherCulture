from django.db import models

# Create your models here.

class Member(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    description = models.TextField()
    attendees = models.IntegerField(default=0)  

    def __str__(self):
        return self.name