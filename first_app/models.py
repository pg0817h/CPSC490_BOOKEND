from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    #TOKEN
    user_token = models.CharField(blank=True,max_length = 10)
    # #additional

    # profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)

    def __str__(self):
        return self.user.username



class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique = True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('first_app:eventDetails', args=(self.id,))


    @property 
    def get_html_url(self):
        url = reverse('first_app:eventDetails', args=(self.id,))
        return f'<a href="{url}">{self.title}</a>'

    
class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default="")
    email = models.EmailField(max_length=100,default="")
    status = models.CharField(max_length=100, default="")

    class Meta:
        # unique_together = ['event', 'user']

        def __str__(self):
            # return str(self.user)
            return str(self.email)

class EventOptions(models.Model):
    # event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    count = models.IntegerField(default=0, blank = True, null = True)
    # event = models.ForeignKey(Event, related_name='options', on_delete=models.SET_NULL, null = True)
    event = models.CharField(max_length=100,default="")


    class Meta:
        
        def __str__(self):
            return self.count

class EventOptions_attendee(models.Model):
    event_option = models.ForeignKey(EventOptions, related_name='options',on_delete=models.SET_NULL, null=True)
    # attendee_email = models.ForeignKey(EventMember, related_name='attendee_email', on_delete=models.SET_NULL, null=True)
    attendee_email = models.EmailField(max_length=100,default="")
    class Meata:
        def __str__(self):
            return self.attendee_email

