from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    my_dict = {'insert_me': "hello i am from views.py!"}
    return render(request,'first_app/index.html',context=my_dict)

def signup(request):
    return render(request, 'signup/signup.html')



def signin(request):
    return render(request, 'signin/signin.html')