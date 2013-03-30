from django.template import Context, loader
from django.http import HttpResponse
from rdtrpr.models import Location
import json

def welcome(request):
	t = loader.get_template('index.html')
	c = Context({
        'current_time': "3PM",
    })
	return HttpResponse(t.render(c))
    
def add_loc(request):
	if request.method == 'POST':
		response_data = {}
		try:
			loc = Location.objects.create_loc(request.POST['lat'], \
				request.POST['long'], request.POST['url'])
			loc.save()
			response_data['result'] = 'success'
			response_data['message'] = 'You did not mess up'
			return HttpResponse(json.dumps(response_data), \
				content_type="application/json")
		except KeyError:
			response_data['result'] = 'failed'
			response_data['message'] = 'You messed up'
			return HttpResponse(json.dumps(response_data), \
				content_type="application/json")