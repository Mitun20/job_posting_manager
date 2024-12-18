from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.department_name

class Roles(models.Model):
    role_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.role_name

class Posts(models.Model):
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    experience_from = models.IntegerField()
    experience_to = models.IntegerField()
    salary = models.CharField(max_length=255)
    close_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='post_images/',null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
