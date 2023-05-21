from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.register,name="signup"),
    path("login/",views.signin,name="login"),
    path("check-username/<str:username>/",views.check_username,name="check_username"),
    path("logout/",views.Logout,name="logout"),
    path("forgot-password/",views.forgot_password,name="forgot_password"),
    path("reset-password/<id>/",views.reset_password,name="reset_password"),
    path("settings/",views.user_settings,name="settings"),
]
