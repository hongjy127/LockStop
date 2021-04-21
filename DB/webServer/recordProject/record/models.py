from django.db import models

# Create your models here.

class Lockdata(models.Model):
    
    topic = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now_add=True,null=True)
    time = models.TimeField(auto_now=True, null=True)
    image = models.BinaryField(null=True)

    class Meta:
        db_table = "lockdata"