

from datetime import datetime, timedelta
import calendar
from .models import Event
from first_project.helper import get_current_user
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
class Calendar(calendar.HTMLCalendar):
	def __init__(self, year=None, month=None, user = None):
		self.year = year
		self.month = month
		self.user = user 
		super(Calendar, self).__init__()

	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		
		d = ''
		
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr id ="week"> {week} </tr>'


	def formatmonth(self, user ,withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user= user)
		
	
		print('this is from utils',events)
	
		cal = f'<table  class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal