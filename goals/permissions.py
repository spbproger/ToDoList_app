from rest_framework import permissions
from goals.models import BoardParticipant, Goal, GoalCategory, Board, GoalComment


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board):
        if not request.user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        if not request.user.is_authenticated:
            return False
        if request.method not in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj,
                role=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
            ).exists()


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        filters: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in permissions.SAFE_METHODS,
            obj.user_id == request.user.id
        ))
