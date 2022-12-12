from rest_framework import serializers
from goals.models import GoalCategory
from core.serializers import ProfileSerializer


class CategoryCreateSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = GoalCategory
		read_only_fields = ("id", "created", "updated", "user")
		fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True)

	class Meta:
		model = GoalCategory
		fields = "__all__"
		read_only_fields = ("id", "created", "updated", "user")

	def validate_category(self, value):
		if value.is_deleted:
			raise serializers.ValidationError('not allowed in deleted category')
		if value.user != self.context['request'].user:
			raise serializers.ValidationError('not owner of category')

		return value