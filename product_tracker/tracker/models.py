from django.db import models
from django.utils.timezone import now

# Create your models here.
class ProductResult(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    img = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    price = models.FloatField()
    created_at = models.DateTimeField(default=now)
    search_text = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class TrackedProducts(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(default=now)
    tracked = models.BooleanField(default=True)

    def __bool__(self):
        return self.tracked
    
