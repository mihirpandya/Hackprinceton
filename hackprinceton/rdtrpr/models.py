from django.db import models
from django.utils import timezone

# Create your models here.

class LocationManager(models.Manager):
	def create_loc(self, lat, lon, url):
		loc = self.create(longitude = lon, latitude = lat, url = url, \
			time = timezone.now())
		return loc
		
class FoursquareManager(models.Manager):
	def create_fsq(self, lid, data):
		fsq = self.create(l_id = lid, tips = data, weather = "n/a")
		return fsq

class WikipediaManager(models.Manager):
	def create_wiki(self, lid, desc, uri):
		wiki = self.create(l_id = lid, data = desc, url = uri)
		return wiki

class Location(models.Model):
	l_id = 	models.AutoField(primary_key=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=7)
	latitude = models.DecimalField(max_digits=10, decimal_places=7)
	url = models.TextField()
	time = models.DateTimeField()
	objects = LocationManager()

class Wikipedia(models.Model):
	w_id = models.AutoField(primary_key=True)
	l_id = models.ForeignKey(Location)
	data = models.TextField()
	url = models.TextField()
	objects = WikipediaManager()

class Foursquare(models.Model):
	f_id = models.AutoField(primary_key=True)
	l_id = models.ForeignKey(Location)
	tips = models.TextField()
	weather = models.TextField()
	objects = FoursquareManager()