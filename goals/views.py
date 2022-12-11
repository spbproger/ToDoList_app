import django_filters
from rest_framework import generics, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from goals import serializers
from .filters import GoalFilter
from .models import GoalCategory, Goal, GoalComment
# from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
# from goals.permissions import BoardPermissions
#from .serializers import GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, \
    #BoardListSerializer

"""
Сериалайзеры для категорий
"""


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCategorySerializer
    #pagination_class = LimitOffsetPagination

    search_fields = ['title']
    ordering_fields = ['title', 'created']
    ordering = ['title']
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    #filterset_fields = ["user"]

    def get_queryset(self):
        return GoalCategory.oblects.filter(user=self.request.user, is_deleted=False)
        # return GoalCategory.oblects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.oblects.filter(user=self.request.user, is_deleted=False)
        # return GoalCategory.oblects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        #with transaction.atomic():
        instance.is_deleted = True
        instance.save()
            #Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


"""
Сериалайзеры для целей
"""


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalSerializer
    #pagination_class = LimitOffsetPagination
    ordering_fields = ['priority', 'due_date']
    ordering = ['-priority', 'due_date']
    search_fields = ['title']
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalFilter

    def get_queryset(self):
        return Goal.oblects.filter(user=self.request.user).exclude(status=Goal.Status.archived)
        # return Goal.oblects.filter(category__board__participants__user=self.request.user).exclude(status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return Goal.oblects.filter(category__board__participants__user=self.request.user)
        return Goal.oblects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GoalCommentSerializer

    ordering_fields = ['goal', 'created', 'updated']
    ordering = ["-created"]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["goal"]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
        # return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
        # return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance

# """
# Доска
# """
# class BoardCreateView(generics.CreateAPIView):
#     model = Board
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.BoardCreateSerializer
#
#
# class BoardView(generics.RetrieveUpdateDestroyAPIView):
#     model = Board
#     permission_classes = [permissions.IsAuthenticated, BoardPermissions]
#     serializer_class = serializers.BoardSerializer
#
#     def get_queryset(self):
#         return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
#
#     def perform_destroy(self, instance: Board):
#         with transaction.atomic():
#             instance.is_deleted = True
#             instance.save()
#             instance.categories.update(is_deleted=True)
#             Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
#         return instance
#
#
# class BoardListView(generics.ListAPIView):
#     model = Board
#     permission_classes = [permissions.IsAuthenticated, BoardPermissions]
#     pagination_class = LimitOffsetPagination
#     serializer_class = serializers.BoardListSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering = ["title"]
#
#     def get_queryset(self):
#         return Board.objects.filter(participants__user=self.request.user, is_deleted=False)