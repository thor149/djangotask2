from django.db import models
from users.models import Profile
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    summary = models.CharField(max_length=15)
    content = models.TextField(null=True, blank=True)
    draft = models.BooleanField(default=False, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

