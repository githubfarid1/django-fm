from django.urls import path
from .views import login_view, register_user, updatePasswordRequest, getngrok
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('update_password/', updatePasswordRequest , name='update_password'),
    path('ngrok/', getngrok , name='getngrok'),

]
