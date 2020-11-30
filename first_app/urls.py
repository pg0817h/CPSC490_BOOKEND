from first_app import views
from django.urls import path 
from django.conf.urls import url


app_name = 'first_app'

urlpatterns = [
  
   
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('', views.index, name="index"),
    
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/getgoogle/', views.get_event_google, name='get_event'),
    path('event/deletegoogle/', views.delete_context_data, name='delete_event'),
   
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path('event/<int:event_id>/details/', views.event_details, name='eventDetails'),
    path('add_eventmember/<int:event_id>', views.add_eventmember, name='add_eventmember'),
    path('event/<int:pk>/remove', views.EventMemberDeleteView.as_view(), name="remove_event"),
    path('event/event_success/', views.event_success, name='event_success'),
    path('event_options/<int:event_id>', views.event_options, name ='event_options'),
    path('event_options/finalize/<int:event_id>',views.finalizeOption, name='finalize_option'),
    path('event_options/finalize/confirm/<int:event_id>',views.confirm_finalize, name='confirm_finalize')
]