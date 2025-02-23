from django.db import models
# from .db_connection import db

# Create your models here.

# userdata = db["auth_app"]


class userdata(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.name
