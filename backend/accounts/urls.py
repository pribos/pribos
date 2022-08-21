from django.urls import path
from . import views
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.google import views as google_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# BASE_URL = 'http://127.0.0.1:8000/'
# GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'


# class GoogleLogin(SocialLoginView):
#     adapter_class = google_view.GoogleOAuth2Adapter
#     callback_url = GOOGLE_CALLBACK_URI
#     client_class = OAuth2Client

urlpatterns = [
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name="google_callback"),
    path('google/finish/', views.GoogleLogin.as_view(), name='google_finish'),
]
