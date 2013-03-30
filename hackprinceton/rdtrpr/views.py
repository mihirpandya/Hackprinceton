from django.template import Context, loader
from django.http import HttpResponse
from rdtrpr.models import *
import json
import urllib
import urllib2

def get_hist(url):
	try:
		res = Location.objects.filter(url=url)
		return map (lambda o: [float(o.latitude), float(o.longitude)], res)
	except Location.DoesNotExist:
		return []

def welcome(request):
	if request.method == 'GET':
		t = loader.get_template('index.html')
		c = Context({
			'a': "test_val",
			})
		return HttpResponse(t.render(c))

def update(request):
	if request.method == 'GET':
		url = request.GET.get('url')
		t = loader.get_template('map.html')
		hist = get_hist(url)
		c = Context({
        	'hist': hist,
    	})
		return HttpResponse(t.render(c))
    
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
			
			if len(d['response']['venues']) > 0:
				print d['response']['venues'][0]['name']
				fsq_lat_err = \
					abs(float(d['response']['venues'][0]['location']['lat']) \
					- float(loc.latitude))
				fsq_lng_err = \
					abs(float(d['response']['venues'][0]['location']['lng']) \
					- float(loc.longitude))
				
				if fsq_lat_err < 0.001 and fsq_lng_err < 0.001:
					fsq = Foursquare.objects.create_fsq(loc, \
						d['response']['venues'][0])
					fsq.save()			
			
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
