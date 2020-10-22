from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from first_app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic 
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar 
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime, date

from .models import *
from .utils import Calendar
from .forms import EventForm

# Create your views here.
def index(request):
       
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        else:   
            my_dict = {'insert_me': "hello i am from views.py!"}
            return render(request,'first_app/index.html',context=my_dict)
@login_required
def dashboard(request):
    return render(request,'first_app/dashboard.html')

@login_required
def special(request):
    return HttpResponse('You are logged in!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print('success')
                # return HttpResponseRedirect(reverse('first_app:signup'))
                return HttpResponseRedirect(reverse('dashboard'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')

        else: 
            print('Someone tried to login and failed!')
            print('Username:{} and password {}'.format(username,password))
            return HttpResponse('Invalid login details supplied!')

    else: 
        return render(request, 'signin/signin.html',{})



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(m):
    first = m.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(m):
    days_in_month = calendar.monthrange(m.year, m.month)[1]
    last = m.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'first_app:signin'
    model = Event
    template_name = 'first_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
     
        d = get_date(self.request.GET.get('month', None))
       
        cal = Calendar(d.year, d.month)
     
        html_cal = cal.formatmonth(withyear=True)
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('first_app:calendar'))
    return render(request, 'first_app/event.html', {'form': form})
class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'event.html'

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'first_app/eventDetails.html', context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data['user']
                EventMember.objects.create(
                    event=event,
                    user=user
                )
                return redirect('first_app:calendar')
            else:
                print('--------------limited-----------------')
    context = {
        'form': forms
    }
    return render(request, 'add_member.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'event_delete.html'
    success_url = reverse_lazy('first_app:calendar')