from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.crypto import get_random_string


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name="id чата")
    tg_user_id = models.BigIntegerField(verbose_name="id пользователя", unique=True)
    tg_username = models.CharField(max_length=30, validators=[MinLengthValidator(8)], blank=True, null=True, verbose_name="Пользователь")
    user = models.ForeignKey('core.User', verbose_name="Пользователь приложения", blank=True, null=True, on_delete=models.CASCADE)
    verification_code = models.CharField(verbose_name="Код верификации", max_length=12, unique=True)

    class Meta:
        verbose_name = "Пользователь Tg"
        verbose_name_plural = "Пользователи Tg"

    def generate_verification_code(self) -> str:
        code = get_random_string(12)
        self.verification_code = code
        self.save()
        return code
