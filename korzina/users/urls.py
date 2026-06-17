from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]