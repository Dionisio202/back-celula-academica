from django.db import models

class Profile(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True ,null=False, blank=False,default='')
    def __str__(self):
        return f"{self.name} {self.last_name}"
