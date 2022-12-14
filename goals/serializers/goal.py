from typing import Type

from rest_framework import serializers, exceptions

from core.serializers import ProfileSerializer
from goals.models import Goal, GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	category = serializers.PrimaryKeyRelatedField(
		queryset=GoalCategory.objects.filter(is_deleted=False)
	)

	class Meta:
		model = Goal
		read_only_fields = ("id", "created", "updated", "user")
		fields = "__all__"

	def validate_category(self, value: GoalCategory):
		if self.context['request'].user_id != value.user.id:
			raise exceptions.PermissionDenied
		if self.instance.category.board_id != value.board.id:
			raise serializers.ValidationError('Transfer between projects not prefer')
		return value


class GoalSerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True)

	class Meta:
		model = Goal
		read_only_fields = ("id", "created", "updated", "user")
		fields = "__all__"

	def validate_category(self, value: GoalCategory):
		if self.context['request'].user_id != value.user.id:
			raise exceptions.PermissionDenied
		return value
