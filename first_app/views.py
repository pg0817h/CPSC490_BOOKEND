from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
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
from .forms import AddMember
import json
from email.mime.text import MIMEText
import base64
# from datetime import date

from datetime import datetime, date


from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
# import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


from .models import *
from .utils import Calendar
from .forms import EventForm



# Create your views here.

def create_message(sender, to, subject, message_content):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """

  message = MIMEText(message_content, 'html')

  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  print(message, 'this is from create')
  b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
  b64_string = b64_bytes.decode() 
  return {'raw': b64_string}


def sendEmail(request,sender,to,subject):
    social_token = SocialToken.objects.get(account__user = request.user,account__provider='google')
        

    creds = Credentials(token = social_token.token,
                            refresh_token = social_token.token_secret,
                            client_id = social_token.app.client_id,
                            client_secret= social_token.app.secret)

        
    service = build('gmail', 'v1', credentials=creds)
    user_id = 'me'
    msg_html = """<html> <head>
    <style>
      .colored {
        color: black;
        font-size: 15px;
      }
      #body {
        font-size: 14px;
      }
      .btn{
          color: white !important;
          background-color: #008CBA;
          text-align: center;
          font-size: 20px;
          border: none;
          padding: 15px 32px;
          text-decoration: none;
          display: inline-block;

      }
    </style>
  </head>
  <body>
    <div id='body'>
      <p class =''>"""f"""Hi,{sender}</p>
      <p class='colored'>{request.user} invites you to participate in the Bookend poll</p>
      <p><a href='http://127.0.0.1:8000/' class='btn'>Participate now </a></p>
      <p>Best wishes,</p>
      <strong>The Bookend Team</strong>

    </div>
  </body>
</html>
    """
  
    message = create_message(sender, to, subject, msg_html)
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message


def index(request):
       
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        else:   
            my_dict = {'insert_me': "hello i am from views.py!"}
            return render(request,'first_app/index.html',context=my_dict)
@login_required
def dashboard(request):
    access_token = SocialToken.objects.get(account__user = request.user, account__provider='google')

    social_token = SocialToken.objects.get(account__user = request.user,account__provider='google')

    creds = Credentials(token = social_token.token,
                        refresh_token = social_token.token_secret,
                        client_id = social_token.app.client_id,
                        client_secret= social_token.app.secret)

    
    service = build('calendar','v3', credentials = creds)
   
    now = datetime.today().isoformat() + 'Z'
    print(now)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
   
    event_dict = {}
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            event_dict[event['summary']] = {}
            event_dict[event['summary']]['start'] = start
            event_dict[event['summary']]['end'] = end
        
      

    return render(request,'first_app/dashboard.html', {'event_dict':event_dict})

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
    # return now


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

def delete_context_data(request):

        context_user = Event.objects.filter(user=request.user).delete()
        print('this is deleted user',context_user)

        return HttpResponseRedirect(reverse('first_app:get_event'))
    
class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'first_app:signin'
    model = Event
    template_name = 'first_app/calendar.html'
   

    def get_context_data(self, **kwargs):
        delete_context_data
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
       
        cal = Calendar(d.year, d.month)
    
        html_cal = cal.formatmonth(self.request.user,withyear=True)
        
        
        context['calendar'] = mark_safe(html_cal)
        
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    


def get_event_google(request):
        social_token = SocialToken.objects.get(account__user = request.user,account__provider='google')
        

        creds = Credentials(token = social_token.token,
                            refresh_token = social_token.token_secret,
                            client_id = social_token.app.client_id,
                            client_secret= social_token.app.secret)

        
        service = build('calendar','v3', credentials = creds)
       
        now = datetime.today().replace(day=1).isoformat() + 'Z'
        
        # eventUpdater = service.events().get(calendarId='primary', eventId=event_Id).execute()
        
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=30, singleEvents=True,
                                        orderBy='startTime').execute()
      
        events = events_result.get('items', [])
     
   
        # print('-----this is events',event__)
        for event in events:
            # print('this is event ',event)
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
          
            # event_ = Event.objects.get(id=event_id)


            # user_ = event['attendees']
       
            Event.objects.get_or_create(
                user=request.user,
                title=event['summary'],
                description=event['summary'],
                start_time=start_time,
                end_time=end_time
            )
            if 'attendees' in event:
               
                for item in event['attendees']:
                    if 'displayName' in item:
                        user_ = item['displayName']
                      
                        user_ = User.objects.get(username=user_)
                        status_ = item['responseStatus']
                      
                        EventMember.objects.create(
                            
                            event=Event.objects.get(title=event['summary']),
                            user=user_,
                            status= status_
                        )

        return HttpResponseRedirect(reverse('first_app:calendar'))
        
  
       
def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']

        # Insert events into google calendar ########
        social_token = SocialToken.objects.get(account__user = request.user,account__provider='google')

        creds = Credentials(token = social_token.token,
                            refresh_token = social_token.token_secret,
                            client_id = social_token.app.client_id,
                            client_secret= social_token.app.secret)

        
        service = build('calendar','v3', credentials = creds)
        now = datetime.today().isoformat() + 'Z'
       
    
        event = {
            'summary': 
                title,
            
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
          
        }
        events_result = service.events().insert(calendarId='primary', body = event ).execute()





        ########


       
            

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
    # print('this is eventmember', eventmember)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'first_app/eventDetails.html', context)


def add_eventmember(request, event_id):
    forms = AddMember()
    
    event = Event.objects.get(id=event_id)
   
    now = datetime.today().replace(day=1).isoformat() + 'Z'
    social_token = SocialToken.objects.get(account__user = request.user,account__provider='google')

    
    creds = Credentials(token = social_token.token,
                            refresh_token = social_token.token_secret,
                            client_id = social_token.app.client_id,
                            client_secret= social_token.app.secret)

        
    service = build('calendar','v3', credentials = creds)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=30, singleEvents=True,
                                        orderBy='startTime').execute()
    
    eventsLists = events_result.get('items', [])
    eventName = Event.objects.get(id=event_id)
   
    if request.method == 'POST':
        forms = AddMember(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            
            user = forms.cleaned_data['user']
           
            for event_ in eventsLists:
               
                if str(event_['summary']) == str(eventName):
                    event_Id = event_['id']
                    
                    eventUpdater = service.events().get(calendarId='primary', eventId=event_Id).execute()
                    if 'attendees' in eventUpdater:
                        eventUpdater['attendees'].insert(0,{'email': user.email, 'displayName': user.username })
                    else:
                        
                        eventUpdater['attendees'] = [  {'email': user.email, 'displayName': user.username }]
                      
                    eventUpdater['reminders'] = {"useDefault": 'false',"overrides":[{'method': 'email', 'minutes': 5}, ]}
                    updated_event = service.events().update(calendarId='primary', eventId = eventUpdater['id'], body = eventUpdater,  sendUpdates='all').execute()
                    print('this is updated event', updated_event)
                    print('attendess',updated_event['attendees'][0]['responseStatus'])




            EventMember.objects.create(
                    event=event,
                    user=user,
                    status= updated_event['attendees'][0]['responseStatus']
            )

            user_ = forms.cleaned_data['user']
            print(str(user_),'this is user name ')

            sendEmail(request,str(user_.username),str(user_.email),str(eventName))

            
            return redirect('first_app:calendar')
           
    context = {
        'form': forms
    }
    return render(request, 'first_app/add_member.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'event_delete.html'
    success_url = reverse_lazy('first_app:calendar')

