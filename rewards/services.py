from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from rewards.models import RewardLog, ScheduledReward
from rewards.tasks import process_scheduled_reward


def get_all_rewards_logs_by_user(user_id: int) -> QuerySet[RewardLog]:
    return RewardLog.objects.filter(user_id=user_id)


def award(user_id: int, amount: int, execute_at: datetime) -> ScheduledReward:
    with transaction.atomic():
        scheduled_reward = ScheduledReward.objects.create(
            user_id=user_id,
            amount=amount,
            execute_at=execute_at,
        )
        
        process_scheduled_reward.apply_async(
            args=[scheduled_reward.id],
            eta=scheduled_reward.execute_at
        )

    return scheduled_reward


def award_myself(user_id: int, amount: int) -> ScheduledReward:
    execute_at = timezone.now() + timedelta(minutes=5)
    return award(
        user_id=user_id,
        amount=amount,
        execute_at=execute_at,
    )
