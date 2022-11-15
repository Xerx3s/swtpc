from django.db import models

class testtable(models.Model):
    Name = models.CharField(max_length=70, blank=False, default='')
    Address = models.CharField(max_length=200,blank=False, default='')
    Date = models.DateField(default='')
