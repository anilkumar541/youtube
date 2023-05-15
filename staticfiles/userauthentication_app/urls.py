from django.urls import path
from .views import registerView, loginView, logoutView
from django.contrib.auth import views as auth_views


app_name= "userauthentication_app"

urlpatterns = [
    path("sign-up/", registerView, name="sign-up"),
    path("sign-in/", loginView, name="sign-in"),
    path("sign-out/", logoutView, name="sign-out"),
    # path("sign-in/", auth_views.LoginView.as_view(template_name= "userauthentication_app/sign-in.html", redirect_authenticated_user=True), name="sign-in"),
    # path("sign-out/", auth_views.LogoutView.as_view(template_name= "userauthentication_app/sign-out.html"), name="sign-out"),
]
