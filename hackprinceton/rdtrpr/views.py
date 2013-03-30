from django.template import Context, loader
from django.http import HttpResponse

def welcome(request):
	t = loader.get_template('map.html')
	c = Context({
        'current_time': "3PM",
    })
	return HttpResponse(t.render(c))