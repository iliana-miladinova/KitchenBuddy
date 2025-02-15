from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, "base.html")
