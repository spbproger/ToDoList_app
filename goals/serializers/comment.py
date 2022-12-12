from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalComment


class CommentCreateSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = GoalComment
		read_only_fields = ('id', 'user', 'created', 'updated', 'goal')
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True)

	class Meta:
		model = GoalComment
		read_only_fields = ('id', 'user', 'created', 'updated', 'goal')
		fields = '__all__'
