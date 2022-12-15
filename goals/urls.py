from django.urls import path
from goals import views

urlpatterns = [
	path("board/create", views.BoardCreateView.as_view(), name="board_create"),
	path("board/list", views.BoardListView.as_view(), name="boards_list"),
	path("board/<pk>", views.BoardView.as_view(), name='board_rud',),

	path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='category_create'),
	path("goal_category/list", views.GoalCategoryListView.as_view(), name='categories_list'),
	path("goal_category/<pk>", views.GoalCategoryView.as_view(), name='category_rud'),

	path("goal/create", views.GoalCreateView.as_view(), name='goal_create'),
	path("goal/list", views.GoalListView.as_view(), name='goals_list'),
	path("goal/<pk>", views.GoalView.as_view(), name='goal_rud'),

	path("goal_comment/create", views.CommentCreateView.as_view(), name='comment_create'),
	path("goal_comment/list", views.CommentListView.as_view(), name='comments_list'),
	path("goal_comment/<pk>", views.CommentView.as_view(), name='comment_rud'),
]
