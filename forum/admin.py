from django.contrib import admin
from forum.models import Tag, Post, Answer, AnswerVote


admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Answer)
admin.site.register(AnswerVote)
