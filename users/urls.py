from django.urls import path

from users.views import SignUpView, SignInView, GoogleLogInView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/google-login', GoogleLogInView.as_view()),
]
