from rest_framework import serializers
from goals.models import GoalCategory, BoardParticipant
from core.serializers import ProfileSerializer


class CategoryCreateSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = GoalCategory
		read_only_fields = ("id", "created", "updated", "user")
		fields = "__all__"

	def validate_board(self, value):
		if value.is_deleted:
			raise serializers.ValidationError('not allowed in deleted category')

		if not BoardParticipant.objects.filter(
				board=value,
				role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
				user=self.context['request'].user
		).exists():
			raise serializers.ValidationError('not allowed for reader')
		return value


class CategorySerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True)

	class Meta:
		model = GoalCategory
		read_only_fields = ("id", "created", "updated", "user", "board")
		fields = "__all__"
