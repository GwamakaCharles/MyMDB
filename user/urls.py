from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path(
    'register',
    views.Registerview.as_view(),
    name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]