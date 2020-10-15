from django.shortcuts import render
from django.http import HttpResponse
from first_app.forms import UserForm

# Create your views here.
def index(request):
    my_dict = {'insert_me': "hello i am from views.py!"}
    return render(request,'first_app/index.html',context=my_dict)

def signup(request):
    registered = False

    if request.method == "POST":

        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()


            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()


    

    return render(request, 'signup/signup.html',{'user_form': user_form, 'registered': registered})



def signin(request):
    return render(request, 'signin/signin.html')