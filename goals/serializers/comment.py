from rest_framework import serializers
from core.serializers import ProfileSerializer
from goals.models import GoalComment, BoardParticipant


class CommentCreateSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = GoalComment
		read_only_fields = ('id', 'created', 'updated', 'user')
		fields = '__all__'

	def validate(self, value):
		if not BoardParticipant.objects.filter(
				board=value['goal'].category.board,
				role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
				user=self.context['request'].user
		).exists():
			raise serializers.ValidationError('Не доступно для прочтения. Только для владельца, либо редактора')
		return value


class CommentSerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True)

	class Meta:
		model = GoalComment
		read_only_fields = ('id', 'user', 'created', 'updated', 'goal')
		fields = '__all__'
