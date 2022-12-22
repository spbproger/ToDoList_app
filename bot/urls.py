from django.urls import path
from bot.views import BotVerificationView

urlpatterns = [
    path("verify", BotVerificationView.as_view(), name="verify"),
]