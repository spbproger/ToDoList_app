from django.db import models
from core.models import User
from django.utils import timezone


class DatesModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        abstract = True


class GoalCategory(DatesModelMixin):
    title = models.CharField(max_length=200, verbose_name='Наименование категории')
    user = models.ForeignKey(User, verbose_name='Автор категории', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(DatesModelMixin):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "В архиве"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(max_length=200, verbose_name='Наименование цели')
    description = models.TextField(verbose_name='Описание цели')
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices, default=Priority.low)
    due_date = models.DateField(verbose_name='Срок исполнения')
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория цели", related_name='goals', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

