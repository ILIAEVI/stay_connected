from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter

from forum.views import PostViewSet, AnswerViewSet

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')

post_router = NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('answers', AnswerViewSet, basename='post-answers')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
]
