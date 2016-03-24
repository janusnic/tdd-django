from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title></html>")

def home(request):
    return render(request, "home/index.html", {})

def req_test(request): 
    output = "<html><title>Welcome to Django.</title><body><p>This is Request Test!</p>"
    mess = request.scheme
    output += 'scheme = '+ mess + '<br>'
    mess = request.path
    output += 'path = '+ mess + '<br>'
    mess = request.path_info
    output += 'path_info = '+ mess + '<br>'
   
    return HttpResponse(output)
    # return HttpResponse("<html><title>Welcome to Django.</title><body><p>This is Request Test!</p></body></html>")