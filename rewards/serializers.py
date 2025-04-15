from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rewards.models import RewardLog, ScheduledReward

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'coins']
        read_only_fields = fields


class RewardLogSerializer(ModelSerializer):
    class Meta:
        model = RewardLog
        fields = ['id', 'amount', 'given_at']
        read_only_fields = fields


class ScheduledRewardSerializer(ModelSerializer):
    class Meta:
        model = ScheduledReward
        fields = ['id', 'amount', 'execute_at']
        read_only_fields = fields
