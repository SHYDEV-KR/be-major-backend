from django.urls import path
from . import views


urlpatterns = [
  path("", views.PortfolioViewSet.as_view({
    "post": "create",
  })),
  path("<int:pk>", views.PortfolioViewSet.as_view({
    "get" : "retrieve",
    "put": "partial_update",
    "delete": "destroy"
  })),
  path("careers/<int:pk>", views.CareerViewSet.as_view({
    "get" : "retrieve",
    "put": "partial_update",
    "delete": "destroy"
  })),

  path("urls", views.UrlViewSet.as_view({
    "post": "create",
  })),

  path("urls/<int:pk>", views.UrlViewSet.as_view({
    "get" : "retrieve",
    "put": "partial_update",
    "delete": "destroy"
  })),
  
  path("education/<int:pk>", views.EducationViewSet.as_view({
    "get" : "retrieve",
    "put": "partial_update",
    "delete": "destroy"
  })),
]