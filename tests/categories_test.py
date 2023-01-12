import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant


@pytest.mark.django_db
def test_create(auth_user: APIClient, add_user: User, board: Board, board_participant: BoardParticipant):
    url = reverse('category_create')

    payload = {
        'title': 'new category',
        'user': add_user.pk,
        'board': board.pk,
    }
    response = auth_user.post(path=url, data=payload)
    response_data = response.json()

    assert response.status_code == 201
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_update(auth_user: APIClient, board: Board, add_user: User, category: GoalCategory) -> None:
    response = auth_user.put(
        reverse("category_rud", args=[category.pk]),
        data=json.dumps({
            "title": "put category",
            "board": board.pk
        }),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.data.get("title") == "put category"



