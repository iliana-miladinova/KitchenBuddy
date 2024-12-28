from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return HttpResponse('<h1>Welcome!</h1>')
