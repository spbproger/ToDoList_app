from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board


class GoalCategoryAdmin(admin.ModelAdmin):
	list_display = ("title", "user", "board", "created", "updated")
	search_fields = ("title", "user", "board")


class GoalAdmin(admin.ModelAdmin):
	list_display = ("title", "user", "category", "created", "updated")
	search_fields = ("title", "user", "category")


class GoalCommentAdmin(admin.ModelAdmin):
	list_display = ("goal", "user", "created", "updated")
	search_fields = ("goal", "user", "text")


class BoardAdmin(admin.ModelAdmin):
	list_display = ("title", "created", "updated")
	search_fields = ("title",)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)

