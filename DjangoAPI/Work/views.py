from django.shortcuts import render

# Create your views here.

def Me(request):
    return render(request, "work/index.html")