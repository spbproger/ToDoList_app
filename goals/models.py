from django.db import models
from django.utils import timezone


class DatesModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


# class Board(DatesModelMixin):
#     class Meta:
#         verbose_name = "Доска"
#         verbose_name_plural = "Доски"
#
#     title = models.CharField(verbose_name="Название", max_length=255)
#     is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


# class BoardParticipant(DatesModelMixin):
#     class Meta:
#         unique_together = ("board", "user")
#         verbose_name = "Участник"
#         verbose_name_plural = "Участники"
#
#     class Role(models.IntegerChoices):
#         owner = 1, "Владелец"
#         writer = 2, "Редактор"
#         reader = 3, "Читатель"
#
#     # board = models.ForeignKey('goals.Board', verbose_name='Доска',
#     #                           on_delete=models.PROTECT, related_name='participants')
#     user = models.ForeignKey('core.User', verbose_name='Пользователь',
#                              on_delete=models.PROTECT, related_name='participants')
#     role = models.PositiveSmallIntegerField(verbose_name='Роль',
#                                             choices=Role.choices, default=Role.owner)


class GoalCategory(DatesModelMixin):
    title = models.CharField(max_length=200, verbose_name='Наименование категории')
    user = models.ForeignKey('core.User', verbose_name='Автор категории', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    # board = models.ForeignKey('goals.Board',
    #                           verbose_name='Доска', on_delete=models.PROTECT,
    #                           related_name='categories')

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(models.Model):
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
    user = models.ForeignKey('core.User', verbose_name='Автор', on_delete=models.PROTECT)
    category = models.ForeignKey('goals.GoalCategory', verbose_name="Категория цели", related_name='goals', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'


class GoalComment(models.Model):

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal,
                             verbose_name="Цель", related_name="comments", on_delete=models.PROTECT)
    user = models.ForeignKey('core.User',
                             verbose_name="Пользователь", related_name="comments", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)