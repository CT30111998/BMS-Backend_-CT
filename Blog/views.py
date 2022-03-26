from django.shortcuts import redirect, render
from .models import Blog
from Blog.models import Blog
from math import ceil

# Create your views here.


def blog(request):

    blogs = Blog.objects.all()
    print(blogs)
    n = len(blogs)
    nSlid = n//4 + ceil((n/4)-(n//4))

    params = {'no_of_slids': nSlid, 'range': range(nSlid), 'blog': blogs}
    return render(request, 'blog/blog.html', params)

