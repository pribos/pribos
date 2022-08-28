from django.urls import path
from . import views

urlpatterns = [
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name="google_callback"),
    path('google/finish/', views.GoogleLogin.as_view(), name='google_finish'),
]

