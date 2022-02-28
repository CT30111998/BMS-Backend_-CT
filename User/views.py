from django.shortcuts import redirect, render
# Create your views here.

def homeView(request):
    return render(request, 'index.html')


def loginView(request):
    return render(request, 'user/login.html')


def login(request):
    return redirect('/')


def signUpView(request):
    return render(request, 'user/signup.html')


def signup(request):
    if request == 'POST':
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        image = request.POST['myFile']
        mNo = request.POST['mNo']
    return redirect('/')


