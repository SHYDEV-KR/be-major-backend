from django.urls import path
from . import views


urlpatterns = [
  path("", views.MoimList.as_view()),
  path("crew-join/<int:crew_join_id>", views.CrewJoin.as_view()),
  path("leader-apply/<int:leader_apply_id>", views.LeaderApply.as_view()),
  path("<int:moim_id>/owner/change-state", views.ChangeMoimCloseState.as_view()),
  path("<int:moim_id>/owner/choose-leader", views.ChooseLeader.as_view()),
  path("<int:moim_id>/owner", views.MoimDetailForOwner.as_view()),
  path("<int:moim_id>/crew-join", views.CrewJoin.as_view()),
  path("<int:moim_id>/leader-apply", views.LeaderApply.as_view()),
  path("<int:moim_id>", views.MoimDetail.as_view()),
]