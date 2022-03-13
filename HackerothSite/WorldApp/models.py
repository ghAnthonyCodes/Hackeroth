from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Repo(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=256)

class Commit(models.Model):
   repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   sha = models.CharField(max_length=512)
   additions = models.IntegerField(default=0)
   deletions = models.IntegerField(default=0)
   total = models.IntegerField(default=0)

