from django import forms 
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo
from django.core import validators 
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, formset_factory, modelformset_factory
from first_app.models import Event, EventMember, EventOptions

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    verify_password = forms.CharField(label="Enter your password again", widget=forms.PasswordInput())

    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        vpassword = all_clean_data['verify_password']

        if password != vpassword:
         
            raise forms.ValidationError(('Make sure password match'))
            
            
    class Meta():
        model = User
        fields = ('username','email','password')



class UserToken(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('user_token',)

class EventOptionForm(forms.ModelForm):
    start_time = forms.DateField(widget=DateInput(attrs= {'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    end_time = forms.DateField(widget = DateInput(attrs= {'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    class Meta:
        model = EventOptions
     
       
        fields = ['start_time','end_time']
EventOptionFormset = modelformset_factory(
    EventOptions,
    fields = ('start_time','end_time'),
    extra =1,
    
    widgets = {
        'start_time': DateInput(attrs= {'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),


    }
)
       


class EventForm(ModelForm):
    class Meta:
        model = Event

        widgets = {
            'start_time': DateInput(attrs= {'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),


        }

        exclude = ['user']


    def __init__(self, *args, **kwargs):
        super(EventForm,self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)




class AddMember(forms.ModelForm):
    email = forms.EmailField(widget = forms.EmailInput())
    name = forms.CharField()
    class Meta:
        model = EventMember
        fields = ['email','name']
        
      
        # fields = ('',)