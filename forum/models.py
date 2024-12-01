from django.db import models
from django.db.models import F
from rest_framework.exceptions import ValidationError
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
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.is_accepted and self.is_rejected:
            raise ValidationError("An answer cannot be both accepted and rejected.")

        super().save(*args, **kwargs)

        if not self.pk:
            Profile.objects.filter(user=self.user).update(total_answers=F('total_answers') + 1)

        if self.is_accepted:
            Profile.objects.filter(user=self.user).update(score=F('score') + 1)
