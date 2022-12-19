from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from goals.models import GoalCategory, GoalComment, Board, Goal
from goals.permissions import BoardPermissions, CategoryPermissions, GoalPermissions, \
    CommentPermissions
from goals.serializers.board import BoardSerializer, BoardCreateSerializer, BoardListSerializer
from goals.serializers.category import CategoryCreateSerializer, CategorySerializer
from goals.serializers.comment import CommentSerializer, CommentCreateSerializer
from goals.serializers.goal import GoalCreateSerializer, GoalSerializer
from goals.filters import GoalDateFilter


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    ordering = ['title']
    search_fields = ('title',)

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['board']
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title",]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goals.update(status=Goal.Status.archived)
            for goal in instance.goals.all():
                goal.status = goal.Status.archived
                goal.save()
        return instance


class GoalCreateView(CreateAPIView):
    #model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "due_date"]
    ordering = ["title"]
    search_fields = ["title", ]

    def get_queryset(self):
        return self.model.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=self.model.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return self.model.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=self.model.Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = self.model.Status.archived
        instance.save()
        instance.save(update_fields=('status', ))
        return instance


class CommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return self.model.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return self.model.objects.filter(
            goal__category__board__participants__user=self.request.user
        )




