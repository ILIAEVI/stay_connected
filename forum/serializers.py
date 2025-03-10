from django.db import transaction
from rest_framework import serializers

from authentication.models import User
from forum.models import Post, Answer, Tag, AnswerVote


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
        }


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = UserDetailSerializer(read_only=True)
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'tags', 'subject', 'body', 'created_at', 'answer_count']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'user': {'read_only': True},
        }

    @staticmethod
    def get_answer_count(obj):
        return obj.answers.count()

    @transaction.atomic
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])

        post = Post.objects.create(**validated_data)
        if tags_data:
            self.update_or_create_tags(tags_data, post)

        return post

    @transaction.atomic
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])

        instance = super().update(instance, validated_data)

        if tags_data:
            self.update_or_create_tags(tags_data, instance)

        return instance

    @staticmethod
    def update_or_create_tags(tags_data, instance):
        tag_names = {tag_data['name'] for tag_data in tags_data}
        existing_tags = Tag.objects.filter(name__in=tag_names)
        existing_tag_names = {tag.name for tag in existing_tags}
        missing_tags = tag_names - existing_tag_names

        if missing_tags:
            Tag.objects.bulk_create((Tag(name=name) for name in missing_tags))

        all_tags = Tag.objects.filter(name__in=tag_names)

        instance.tags.set(all_tags)


class AnswerVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerVote
        fields = ['answer', 'vote_type']

    def validate(self, attrs):
        user = self.context['request'].user
        answer = attrs.get('answer')

        try:
            answer = Answer.objects.get(id=answer.id)
        except Answer.DoesNotExist:
            raise serializers.ValidationError('Answer does not exist')

        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='total_likes', read_only=True)
    dislikes = serializers.IntegerField(source='total_dislikes', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'user', 'body', 'created_at', 'is_accepted', 'likes', 'dislikes']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'is_accepted': {'read_only': True},
        }


class AnswerMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['is_accepted']

    def validate(self, attrs):
        if attrs.get('is_accepted', False):
            answer = self.instance
            if Answer.objects.filter(post=answer.post, is_accepted=True).exclude(pk=answer.pk).exists():
                raise serializers.ValidationError("Another answer is already marked as accepted for this post.")
        return attrs
