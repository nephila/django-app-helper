# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user():
    user = User.objects.create(username='foo')
    assert user.pk
