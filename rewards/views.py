from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rewards import services
from rewards.serializers import (
    RewardLogSerializer,
    ScheduledRewardSerializer,
    UserSerializer,
)


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RewardLogListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RewardLogSerializer

    def get_queryset(self):
        return services.get_all_rewards_logs_by_user(user_id=self.request.user)


class RequestRewardView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        scheduled_reward = services.award_myself(
            user_id=request.user.id,
            amount=settings.DEFAULT_AMOUNT_SELF_AWARDING
        )
        
        serializer = ScheduledRewardSerializer(data=scheduled_reward)  
        serializer.is_valid() 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
