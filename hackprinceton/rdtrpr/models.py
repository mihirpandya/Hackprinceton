from django.db import models

# Create your models here.

class Location(models.Model):
	l_id = 	models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    url = models.TextField()
    time = models.DateField()

class Wikipedia(models.Model):
	w_id = models.AutoField(primary_key=True)
	l_id = models.ForeignKey(Location)
	data = models.TextField()
	url = models.TextField()

class Foursquare(models.Model):
	f_id = models.AutoField(primary_key=True)
	l_id = models.ForeignKey(Location)
	tips = models.TextField()
	weather = models.TextField()