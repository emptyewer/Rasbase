from django.shortcuts import render
from django.contrib.auth.models import User
from submitter.models import Submitter

def search(request):
    return render(request, "search/search.html")
