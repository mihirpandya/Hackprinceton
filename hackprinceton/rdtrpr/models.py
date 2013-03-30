from django.db import models

# Create your models here.

class LocationManager(models.Manager):
    def create_loc(self, id, lat, long, url, time):
        loc = self.create(l_id = id, longitude = long, latitude = lat, url = url, time = time)
        
        return loc

class Location(models.Model):
	l_id = 	models.AutoField(primary_key=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=7)
	latitude = models.DecimalField(max_digits=10, decimal_places=7)
	url = models.TextField()
	time = models.DateField()
	objects = LocationManager()

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