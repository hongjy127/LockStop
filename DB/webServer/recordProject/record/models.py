from django.db import models

from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Lockdata(models.Model):
    
    topic = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now_add=True,null=True)
    time = models.TimeField(auto_now=True, null=True)
    image = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "lockdata"

    
    def __str__(self):
        return self.image

    def get_absolute_url(self):
        return reverse('detail', args=(self.id,))

    def get_previous(self):
        return self.get_previous_by_mod_date()

    def get_next(self):
        return self.get_next_by_mod_date()

    def no_has_next(self):
        return reverse('record/todaylist.html')