from django.conf import settings
from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = "Runs Telegram bot"
    tg_client = TgClient(settings.BOT_TOKEN)
    offset = 0

    # def choose_categories(self, msg: Message, tg_user: TgUser):
    #     pass

    def choose_category(self, msg: Message, tg_user: TgUser):
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goal_categories_srt = "\n".join(["🔹 " + goal.title for goal in goal_categories])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"🏷 Выберите категорию:\n"
                 f"=====================\n"
                 f"{goal_categories_srt}\n"
                 f"=====================\n"
        )

        # ожидание категории от пользователя
        is_running = True

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)

            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, "message"):
                    category = goal_categories.filter(title=msg.text)
                    if category:
                        self.create_goal(msg, tg_user, category)
                        is_running = False
                    elif msg.text == "/cancel":
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text="Действие отменено ☹!"
                        )
                        is_running = False
                    else:
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f"Категории с названием {msg.text} не существует ☹!"
                        )
                        is_running = False

    def create_goal(self, msg: Message, tg_user: TgUser, category: GoalCategory):

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text="Введите название цели для ее создания!"
        )

        # ожидания цели от пользователя
        is_running = True

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)

            for item in res.result:
                self.offset = item.update_id + 1
                if item.message.text == "/cancel":
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text="Действие отменено ☹!"
                    )
                    is_running = False
                else:
                    goal = Goal.objects.create(
                        title=item.message.text,
                        category=category,
                        user=tg_user.user,
                    )
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f"Цель успешно {goal.title} добавлена👍!"
                    )
                    is_running = False

    def get_goals(self, msg: Message, tg_user: TgUser):
        """
        Получение всех целей пользователя в Telegram.
        Если целей у пользователя нет, то отправить сообщение, что целей нет.
        """
        goals = Goal.objects.filter(category__board__participants__user=tg_user.user).exclude(
            status=Goal.Status.archived)

        if not goals:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"На сегодня целей нет")
            return None

        goals_str = "\n".join(["🔹 " + goal.title for goal in goals])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"📌 Ваш список целей:\n"
                 f"===================\n"
                 f"{goals_str}:\n"
                 f"===================\n"
        )

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.msg_from.id,
            tg_chat_id=msg.chat.id,
            tg_username=msg.chat.username,
        )

        if created:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Для подтверждения аккаунта\n"
                     f"введите код проверки:\n\n"
                     f"{tg_user.verification_code}\n\n"
                     f"на сайте pesaulov87.ga"
            )
        if msg.text == "/goals":
            self.get_goals(msg, tg_user)

        elif msg.text == "/create":
            self.offset += 1
            self.choose_category(msg, tg_user)

        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"⛔ Вы ввели неизвестную команду ( ** {msg.text} ** )!"
            )
        # else:
        #     self.tg_client.send_message(
        #         chat_id=msg.chat.id,
        #         text="Ваш аккаунт уже был подтвержден!"
        #     )

    def handle(self, *args, **options):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)

            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, "message"):
                    self.handle_message(item.message)