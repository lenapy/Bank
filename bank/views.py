from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bank import models

def index(request):
    return render(request, 'index.html')
