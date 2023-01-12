import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from goals.models import GoalComment, Goal
from goals.serializers.comment import CommentSerializer


@pytest.mark.django_db
def test_create(auth_user: APIClient, add_user: User, goal: Goal) -> None:
    url = reverse('comment_create')

    payload = {
        'text': 'new comment',
        'user': add_user.pk,
        'goal': goal.pk,
    }
    response = auth_user.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == 201
    assert response_data['text'] == payload['text']


@pytest.mark.django_db
def test_retrieve(auth_user: APIClient, add_user: User, comment: GoalComment, goal: Goal) -> None:
    response = auth_user.get(reverse("comment_rud", args=[comment.pk]))

    expected_response = CommentSerializer(instance=comment).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_user: APIClient, goal: Goal, comment: GoalComment) -> None:
    response = auth_user.delete(reverse("comment_rud", args=[comment.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_user: APIClient, goal: Goal, add_user: User, comment: GoalComment) -> None:
    response = auth_user.put(
        reverse("comment_rud", args=[comment.pk]),
        data=json.dumps({
            "text": "put comment",
            "goal": goal.pk
        }),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.data.get("text") == "put comment"
