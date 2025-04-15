from django.contrib import admin
from rewards.models import ScheduledReward, RewardLog, User
from rewards.tasks import process_scheduled_reward


@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'execute_at']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    date_hierarchy = 'execute_at'
    autocomplete_fields = ['user']
    
    def save_model(self, request, obj, form, change):
        process_scheduled_reward.apply_async(
            args=[obj.id],
            eta=obj.execute_at
        )
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'coins']
    list_display = ['username', 'email', 'coins']


admin.site.register(RewardLog)
