from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


    # class Meta:
    #     verbose_name = "Категория"
    #     verbose_name_plural = "Категории"
    #
    # def __str__(self):
    #     return self.name
