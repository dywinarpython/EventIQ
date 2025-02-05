from django.urls import path
from .views import *
app_name = 'event'
urlpatterns = [
    path('', IndexTemplate.as_view(), name='home'),
    path('FAQ/', FAQ_Template.as_view(), name='FAQ'),
    path('events/', My_events_Template.as_view(), name='my_events'),
    path('event_detail/<slug:slug_event>',
         EventDetailView.as_view(), name='event_detail'),
    path('create_event/', Create_event.as_view(),
         name='create_event'),
    path('event_delete/<slug:slug_event>',
         EventDelete.as_view(), name='event_delete'),
    path('contact/', SupportForm.as_view(), name='contact')
]
