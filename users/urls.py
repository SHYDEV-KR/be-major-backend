from django.urls import path, include
from . import views

urlpatterns = [
  path("sms-auth/", views.SMSAuthView.as_view()),
  path("join", views.UserCreate.as_view()),
  path("api-auth/", include("rest_framework.urls")),
  path("log-in", views.LogIn.as_view()),
  path("my-account", views.MyAccount.as_view()),
  path("change-password", views.ChangePassword.as_view()),
  path("log-out", views.LogOut.as_view()),
  path("profile", views.UserProfileViewSet.as_view({
    "post": "create",
  })),
  path("my-profile", views.MyProfile.as_view()),
  path("my-moims", views.MyMoims.as_view()),
  path("@<str:username>", views.PublicUserProfile.as_view()),
  path("@<str:username>/portfolios", views.UserPortfolio.as_view()),
  path("@<str:username>/careers", views.UserCareers.as_view()),
  path("@<str:username>/urls", views.UserUrls.as_view()),
  path("@<str:username>/education", views.UserEducation.as_view()),
  path("@<str:username>/moims/crew", views.UserMoimAsCrew.as_view()),
  path("@<str:username>/moims/leader", views.UserMoimAsLeader.as_view()),
]