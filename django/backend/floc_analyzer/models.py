from django.db import models

class addTwoNumberData(models.Model):
    firstnum = models.FloatField(max_length=1, blank=False, default='0')
    secondnum = models.FloatField(max_length=1, blank=False, default='0')