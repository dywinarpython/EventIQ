from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from event_search.views import pagenotfound, server_is_not_good, server_is_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('event_search.urls', namespace='event')),
    path('', include('users.urls', namespace='users'))
]


handler404 = pagenotfound
handler505 = server_is_not_good
handler500 = server_is_500
admin.site.site_header = "Панель администрирования EventIQ"
