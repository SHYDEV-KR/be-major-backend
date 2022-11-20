from django.urls import path
from . import views


urlpatterns = [
  path("", views.MoimList.as_view()),
  path("<int:moim_id>", views.MoimDetail.as_view()),
]