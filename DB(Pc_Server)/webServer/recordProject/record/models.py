from django.db import models

# Create your models here.

class Lock(models.Model):


    class Meta:
        managed = False
        db_table = 'lockdata'

        def __str__(self):
            return self.title

        def get_absolute_url(self): # 현재 데이터의 절대 경로 추출
            #return reverse('blog:detail', args=(self.slug,))
            return reverse('blog:detail', args=(self.id,))