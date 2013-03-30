from django.template import Context, loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rdtrpr.models import *
import json
import urllib
import urllib2
import random
import string
import ast

def get_hist(url):
	try:
		res = Location.objects.filter(url=url)
		return map (lambda o: [float(o.latitude), float(o.longitude)], res)
	except Location.DoesNotExist:
		return []

# returns latest tips attribute for corresponding URL
def get_foursquare(url):
	objs = Location.objects.filter(url=url)
	result = []
	if(len(objs) > 0):
		objs = Location.objects.filter(url=url)
		l_id = objs[len(objs)-1]
		try:
			tip = ast.literal_eval(Foursquare.objects.get(l_id=l_id.l_id).tips)
			result.append(tip['name'])
			result.append(tip['location']['city']+", "+tip['location']['country'])
		except Foursquare.DoesNotExist:
			return result
		try:
			data = Wikipedia.objects.get(l_id=l_id.l_id).data
			result.append(data)
			return result
		except Wikipedia.DoesNotExist:
			return result
	else:
		return result

def welcome(request):
	t = loader.get_template('index.html')
	c = Context({'dummy': "dummy"})
	return HttpResponse(t.render(c))

def tracker(request):
	if request.method == 'GET':
		url = request.GET.get('url')
		t = loader.get_template('map.html')
		hist = get_hist(url)
		foursquare = get_foursquare(url)
		print foursquare
		c = Context({
        	'hist': hist,
        	'data': foursquare,
    	})
		return HttpResponse(t.render(c))
		
def start(request):
	if request.method == 'POST':
		# generate id
		
		while True:
			try:
				turl = ''.join(random.choice(string.ascii_lowercase + \
					string.digits) for x in range(10))
				
				Location.objects.get(url=turl)
			except ObjectDoesNotExist:
				break
		
		return HttpResponse(turl, \
			content_type="application/json")
    
def add_loc(request):
	if request.method == 'POST':
		response_data = {}
		try:
			# save to db
			loc = Location.objects.create_loc(request.POST['lat'], \
				request.POST['long'], request.POST['url'])
			loc.save()
			
			# foursquare
			query = urllib.urlencode(dict(ll = str(loc.latitude) + "," + \
				str(loc.longitude), client_id = \
				"NTXGIW3A3ZUDBWKYT1EHHSJZF35KU2W0U4Z5ZAR5GUAYGHXI", \
				client_secret = \
				"SQ0CZIH4X4FJLZOHBGPUQHPPQDJBZMOT2MFW5DP3P3JPMVZ2", v = \
				"20130330", intent = "checkin"))
				
			resp = \
				urllib2.urlopen("https://api.foursquare.com/v2/venues/search?" \
				+ query)
			d = json.load(resp)
			
			fsq = None
			if len(d['response']['venues']) > 0:
				fsq_lat_err = \
					abs(float(d['response']['venues'][0]['location']['lat']) \
					- float(loc.latitude))
				fsq_lng_err = \
					abs(float(d['response']['venues'][0]['location']['lng']) \
					- float(loc.longitude))
				
				if fsq_lat_err < 0.001 and fsq_lng_err < 0.001:
					print d['response']['venues'][0]['name']
					fsq = Foursquare.objects.create_fsq(loc, \
						d['response']['venues'][0])
					fsq.save()
					
			# wikipedia
			query = urllib.urlencode(dict(lat = str(loc.latitude), lng = \
				str(loc.longitude), radius = '100', limit = '3'))
			
			resp = urllib2.urlopen("http://api.wikilocation.org/articles?" \
				+ query)
			d = json.load(resp)
			
			saved = None
			for entry in d['articles']:
				if entry['type'] in ['airport', 'city', 'edu', 'forest', \
					'glacier', 'isle', 'landmark', 'mountain', 'pass', \
					'railwaystation', 'waterbody']:
					if saved == None:
						saved = entry
					else:
						if saved['distance'] == entry['distance'] and \
							int(saved['id']) > int(entry['id']):
							saved = entry
							
			if saved == None:
				query = urllib.urlencode(dict(lat = str(loc.latitude), lng = \
					str(loc.longitude), radius = '10000', limit = '1', type = 'city'))
			
				resp = urllib2.urlopen("http://api.wikilocation.org/articles?" \
					+ query)
				d = json.load(resp)
				
				if len(d['articles']) > 0:
					saved = d['articles'][0];
			
			if saved != None:
				query = "http://dbpedialite.org/things/" + saved['id']
				resp = urllib2.urlopen(query + ".json")
				d = json.load(resp)
			
				data = d[query + "#id"]\
					["http://www.w3.org/2000/01/rdf-schema#comment"][0]["value"]
				
				wiki = Wikipedia.objects.create_wiki(loc, data, saved["url"])
				wiki.save()
						
			response_data['result'] = 'success'
			response_data['message'] = 'You did not mess up'
			return HttpResponse(json.dumps(response_data), \
				content_type="application/json")
		except KeyError:
			print 'Where is my url?'
			return HttpResponse("error", mimetype="application/json")
			response_data['result'] = 'failed'
			response_data['message'] = 'You messed up'
			return HttpResponse(json.dumps(response_data), \
				content_type="application/json")
