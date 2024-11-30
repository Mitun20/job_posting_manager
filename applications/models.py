from django.db import models
from account.models import Posts
# Create your models here.

class Application(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    additional_info = models.TextField(blank=True, null=True)
    cv_file = models.FileField(upload_to='cv_files/')
    applied_on = models.DateField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Schedule Interview', 'Schedule Interview'),
        ('Waiting for Results', 'Waiting for Results'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.post.title}"