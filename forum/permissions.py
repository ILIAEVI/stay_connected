from rest_framework import permissions


class IsPostOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.user == request.user:
            return True


class IsAnswerAuthorOrPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        current_user = request.user
        if obj.user == current_user:
            return True

        if request.method == 'DELETE' and obj.post.user == current_user:
            return True


class CanMarkAnswer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        post__user = obj.post.user

        if obj.user == post__user or obj.user == request.user:
            return False

        return True
