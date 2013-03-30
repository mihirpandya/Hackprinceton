from django.template import Context, loader
from django.http import HttpResponse

def welcome(request):
	t = loader.get_template('index.html')
	c = Context({
        'current_time': datetime.now(),
    })
	return HttpResponse(t.render(c))