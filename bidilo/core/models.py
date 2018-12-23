from django.db import models

# Create your models here.

class Auction(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    pub_date = models.DateTimeField('Date Published')
    base_price = models.PositiveIntegerField(default=0)
    deadline = models.DateTimeField()