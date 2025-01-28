from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.TextField(max_length=500,blank=True)
    address_line_2 = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(upload_to="userprofile",blank=True,null=True)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    zipcode = models.IntegerField(max_length = 10,null=True)
    phoneno = models.IntegerField(max_length=10,null=True)

    def __str__(self):
        return self.user.first_name