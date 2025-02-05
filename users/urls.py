from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
app_name = 'users'
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='event:home'), name='logout', ),
    path('registration/', Registrtion_View.as_view(), name='registration'),
    path('verify_email/', Verify_email.as_view(), name='verify_email')
]
