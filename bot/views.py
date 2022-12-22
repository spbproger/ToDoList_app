from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TgUser
from .serializers import TgUserSerializer
from .tg.client import TgClient


class BotVerificationView(generics.UpdateAPIView):
    model = TgUser
    permission_classess = [IsAuthenticated]
    serializer_class = TgUserSerializer
    http_method_names = ["patch"]

    # def get_object(self):
    #     try:
    #         obj = self.model.objects.get(verification_code=self.request.data.get("verification_code"))
    #     except self.model.DoesNotExist:
    #         raise ValidationError("Введен неверный код верификации!")
    #
    #     return obj

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient(settings.BOT_TOKEN)
        tg_user = TgUser.objects.filter(verification_code=data["verification_code"]).first()

        if not tg_user:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        tg_user = request.user
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text="Good!")
        return Response(data=data, status=status.HTTP_200_OK)
