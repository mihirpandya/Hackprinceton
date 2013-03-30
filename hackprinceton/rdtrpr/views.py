from django.template import Context, loader
from django.http import HttpResponse
from rdtrpr.models import *
import json

def get_hist(url):
	try:
		res = Location.objects.filter(url=url)
		return map (lambda o: [float(o.latitude), float(o.longitude)], res)
	except Location.DoesNotExist:
		return []

def welcome(request):
	if request.method == 'GET':
		url = request.GET.get('url')
		t = loader.get_template('map.html')
		hist = get_hist(url)
		print hist
		c = Context({
        	'hist': hist,
    	})
		return HttpResponse(t.render(c))
    
def add_loc(request):
	if request.method == 'POST':
		response_data = {}
		try:
			loc = Location.objects.create_loc(request.POST['lat'],request.POST['long'], request.POST['url'])
			loc.save()
			response_data['result'] = 'success'
			response_data['message'] = 'You did not mess up'
			return HttpResponse(json.dumps(response_data),content_type="application/json")
		except KeyError:
			print 'Where is my url?'
			return HttpResponse("error", mimetype="application/json")
			response_data['result'] = 'failed'
			response_data['message'] = 'You messed up'
			return HttpResponse(json.dumps(response_data),content_type="application/json")
