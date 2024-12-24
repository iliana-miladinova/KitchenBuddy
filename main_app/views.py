from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def index(request):
    return HttpResponse('<h1>Welcome!</h1>')
