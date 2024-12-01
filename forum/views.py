from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from forum.models import Post, Answer
from forum.permissions import IsOwnerOrReadOnly
from forum.serializers import PostSerializer, AnswerSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    query_string = 'user'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    query_string = 'user'

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise ValidationError("Post not found")
        serializer.save(post=post, user=self.request.user)

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return self.queryset.filter(post_id=post_pk)

    @action(
        detail=True,
        methods=['POST'],
        url_path='mark-as-accepted',
        permission_classes=[IsOwnerOrReadOnly],
        query_string='post__user'
    )
    def mark_as_accepted(self, request, pk=None, post_pk=None):
        answer = Answer.objects.select_related('post__user', 'user').get(pk=pk)
        if answer.user == answer.post.user:
            raise ValidationError("You can't mark your answer as accepted")
        answer.is_accepted = True
        answer.save()
        return Response({'detail': 'answer is marked as accepted'}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        url_path='mark-as-rejected',
        permission_classes=[IsOwnerOrReadOnly],
        query_string='post__user'
    )
    def mark_as_rejected(self, request, pk=None, post_pk=None):
        try:
            answer = Answer.objects.select_related('post__user', 'user').get(pk=pk)
        except Answer.DoesNotExist:
            raise ValidationError("Answer not found")
        if answer.user == answer.post.user:
            raise ValidationError("You can't mark your answer as rejected")
        answer.is_rejected = True
        answer.save()
        return Response({'detail': 'answer is marked as rejected'}, status=status.HTTP_200_OK)

