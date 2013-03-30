from django.template import Context, loader
from django.http import HttpResponse

def welcome(request):
	t = loader.get_template('index.html')
	c = Context({
        'current_time': "3PM",
    })
	return HttpResponse(t.render(c))
    
def add_loc(request):
	if request.method == 'POST':
		try:
			print request.POST['url']
			return HttpResponse(request.POST['url'], mimetype="application/json")
		except KeyError:
			print 'Where is my url?'
			return HttpResponse("error", mimetype="application/json")