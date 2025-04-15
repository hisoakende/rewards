from celery import shared_task
from django.db import transaction
from django.db.models import F
from rewards.models import RewardLog, ScheduledReward, User


@shared_task(bind=True)
def process_scheduled_reward(self, reward_id):
    try:
        with transaction.atomic():
            reward = ScheduledReward.objects.get(id=reward_id)
            User.objects.filter(id=reward.user_id).update(coins=F('coins') + reward.amount)
            RewardLog.objects.create(
                user_id=reward.user_id,
                amount=reward.amount
            )

    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)
