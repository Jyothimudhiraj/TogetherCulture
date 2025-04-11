from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date

class CustomUser(models.Model):
    STATUS_CHOICES = (
        (0, 'No Membership'),
        (1, 'Pending Approval'),
        (2, 'Approved'),
    )
    full_name = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    membershipStatus = models.IntegerField(choices=STATUS_CHOICES, default=0)
    membershipType = models.CharField(max_length=255, blank=True, null=True)
    interests = models.JSONField(default=list) 


    def __str__(self):
        return f"{self.full_name} - {self.interests}"
    
    def update_membership_status(self, new_status):
        """Updates the membership status for the user."""
        if new_status in [0, 1, 2]:
            self.membershipStatus = new_status
            self.save()

class Interests(models.Model):
    @staticmethod
    def get_Interests():
        return ['Reading Books', 'Listing to podcasts', 'Painting', 'Travelling', 'Cooking', 'Gardening', 'Photography', 'Writing', 'Music', 'Sports', 'Fitness', 'Technology', 'Fashion', 'Food', 'Health & Wellness']
    
class Benefits(models.Model):
    @staticmethod
    def get_benefits():
        return {
            'T1': ['Community Newsletter', 'Exclusive Forum Access'],
            'T2': ['Monthly Workshops', 'Resource Library', 'Webinars', 'Networking Events'],
            'T3': ['All other membership Benefits', 'Personal Mentorship', 'Advanced Skill Courses', 'Annual Retreat', 'Swag Kit', 'Priority Event Access']
        }
class UserInterests(models.Model):
    user = ''
    UserInterests = []

class UserBenefits(models.Model):
    userBenefits = {}


class AllEvents(models.Model):
    class Meta:
        verbose_name = "AllEvent"
        verbose_name_plural = "AllEvents"
        
    
    name = models.CharField(max_length=200)
    description = models.TextField() 

    def __str__(self):
        return self.name
    
from django.shortcuts import render
from django.db.models import Q
from .models import CustomUser

def search_members(request):
    query = request.GET.get('query', '')
    members = CustomUser.objects.filter(
        Q(full_name__icontains=query) | Q(email__icontains=query)
    ) if query else CustomUser.objects.all()

    return render(request, 'AdminDashboard.html', {
        'members': members,
        'Total_Members': members.count(),
    })



class DigitalContent(models.Model):
    ACCESS_CHOICES = (
        ('T1', 'Tier 1'),
        ('T2', 'Tier 2'),
        ('T3', 'Tier 3'),
    )
    id = models.AutoField(primary_key=True)
    contentName = models.CharField(max_length=255)
    contentDescription = models.TextField()
    createdDate = models.DateField(auto_now_add=True)
    accessBy = models.CharField(max_length=2, choices=ACCESS_CHOICES)
    image = models.ImageField(upload_to='digital_content_images/', blank=True, null=True)   
    def __str__(self):
        return self.contentName


class RegisteredDigitalContent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    digitalContent = models.ForeignKey(DigitalContent, on_delete=models.CASCADE)
    registeredDate = models.DateField(auto_now_add=True)  # Ensure this is present
    def __str__(self):
        return f"{self.user.full_name} - {self.digitalContent.contentName}"