from django.db import connection
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from forum.models import Post, Answer
from forum.permissions import CanMarkAnswer, IsAnswerAuthorOrPostOwner, IsPostOwnerOrReadOnly
from forum.serializers import PostSerializer, AnswerSerializer, AnswerMarkSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related('tags').select_related('user')
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAnswerAuthorOrPostOwner]

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise ValidationError("Post not found")
        serializer.save(post=post, user=self.request.user)

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Answer.objects.filter(post_id=post_pk).select_related('post', 'user')

    @action(
        detail=True,
        methods=['PATCH'],
        url_path='mark-answer',
        url_name='mark-answer',
        permission_classes=[CanMarkAnswer],
        serializer_class=AnswerMarkSerializer
    )
    def mark_answer(self, request, pk=None, post_pk=None):
        try:
            answer = Answer.objects.select_related('post__user', 'user__profile').get(pk=pk)
        except Answer.DoesNotExist:
            raise ValidationError("Answer not found")

        self.check_object_permissions(request, answer)

        serializer = self.get_serializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
