from django.db import models
from django.utils.crypto import get_random_string


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name="id чата")
    tg_user_id = models.BigIntegerField(verbose_name="id пользователя", unique=True)
    user = models.ForeignKey('core.User',
                             verbose_name="Пользователь приложения",
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE
                             )
    verification_code = models.CharField(verbose_name="Код верификации",
                                         max_length=15,
                                         unique=True,
                                         null=True,
                                         blank=True
                                         )

    class Meta:
        verbose_name = "Пользователь Tlgrm"
        verbose_name_plural = "Пользователи Tlgrm"

    def generate_verification_code(self):
        code = get_random_string(12)
        self.verification_code = code
        self.save()

