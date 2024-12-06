from django.db import models, transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from authentication.models import User, Profile


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name="posts")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="answers")
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.votes.filter(vote_type=AnswerVote.VoteChoices.LIKE).count()

    @property
    def total_dislikes(self):
        return self.votes.filter(vote_type=AnswerVote.VoteChoices.DISLIKE).count()


class AnswerVote(models.Model):

    class VoteChoices(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_votes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.SmallIntegerField(choices=VoteChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')





@receiver(post_save, sender=Answer)
def update_answer_count_on_save(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            profile = instance.user.profile
            profile.total_answers += 1
            profile.save()


@receiver(post_delete, sender=Answer)
def update_answer_count_on_delete(sender, instance, **kwargs):
    with transaction.atomic():
        profile = instance.user.profile
        profile.total_answers -= 1
        profile.save()
