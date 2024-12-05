from django.db import transaction
from rest_framework import serializers
from forum.models import Post, Answer, Tag, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'tags', 'subject', 'body', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'user': {'read_only': True},
        }

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


class AnswerLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'answer', 'value']
        extra_kwargs = {
            'user': {'read_only': True},
            'answer': {'read_only': True},
        }


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'user', 'body', 'created_at', 'is_accepted']
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
