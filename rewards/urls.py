from django.urls import path
from rewards.views import (
    ProfileView,
    RewardLogListView,
    RequestRewardView,
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('rewards/', RewardLogListView.as_view(), name='reward-list'),
    path('rewards/request/', RequestRewardView.as_view(), name='request-reward'),
]
