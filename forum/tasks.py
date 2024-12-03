from celery import shared_task
from django.db import transaction
from django.db.models import Count, F
from authentication.models import Profile


@shared_task
def calculate_user_scores():
    print('Calculating user scores...')
    with transaction.atomic():
        profiles = Profile.objects.annotate(
            accepted_answers_count=Count('user__answers', filter=F('user__answers__is_accepted')),
        )

        profiles_to_update = (
            Profile(id=profile.id, score=profile.accepted_answers_count)
            for profile in profiles
        )
        Profile.objects.bulk_update(profiles_to_update, ['score'])
