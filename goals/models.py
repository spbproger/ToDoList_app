from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда модель только создается – у нее нет id
            self.created = timezone.now()
        self.updated = timezone.now()  # Каждый раз, когда вызывается save, проставляем свежую дату обновления
        return super().save(*args, **kwargs)


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Заголовок", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет",
        choices=Priority.choices,
        default=Priority.medium
    )
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goals")
    category = models.ForeignKey(GoalCategory, on_delete=models.CASCADE)


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT, related_name="goal_comments")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="goal_comments")

