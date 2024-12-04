import django_filters
from forum.models import Post, Tag, Answer


class PostFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__name',
        queryset=Tag.objects.all(),
        to_field_name='name'
    )

    subject = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['subject', 'tags']


class AnswerFilter(django_filters.FilterSet):
    class Meta:
        model = Answer
        fields = ['is_accepted']