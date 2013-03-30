from django.template import Context, loader
from django.http import HttpResponse
from rdtrpr.models import *

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