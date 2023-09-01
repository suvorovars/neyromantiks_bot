import asyncio

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from db.tasks import Task
from vk_bot.vk_bot_function import *

from db import db_session

import constants

db_session.global_init(constants.db_location)

USERS_IN_MESSAGE_SEQUENCE = {}


# TODO проверить работоспособность кода, оптимизировать
# Обработчик сообщений
async def message_reply(vk: VkApiMethod, event: VkEventType.MESSAGE_NEW) -> None:
    global USERS_IN_MESSAGE_SEQUENCE
    if event.text == 'Подать заявку':
        vk.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            message="Введите вашу заявку в рамках одного сообщения. Приложите к этому сообщению все нужные файлы "
        )
        USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 1
    elif event.text == "Проверить состояние заявок":
        session = db_session.create_session()
        tasks = session.query(Task).filter(Task.user_id == event.user_id)
        print(tasks)

        # TODO Реализовать Вывод Задач

    elif event.user_id in USERS_IN_MESSAGE_SEQUENCE.keys():
        if USERS_IN_MESSAGE_SEQUENCE[event.user_id] == 1:
            session = db_session.create_session()
            task = Task()
            task.user_id = event.user_id
            task.task = event.text
            task.files = ''  # TODO здесь нужно закинуть ссылки на файлы
            session.add(task)

            vk.messages.send(
                peer_id=event.user_id,
                random_id=get_random_id(),
                keyboard=create_keyboard('Да', "Нет").get_keyboard(),
                message='Это всё, идём дальше?'
            )

            USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 2

        elif USERS_IN_MESSAGE_SEQUENCE[event.user_id] == 2:
            if event.text.lower() == "да":
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=create_keyboard().get_keyboard(),
                    message="Ваша заявка принята в обработку, ожидайте ответа администратора"
                )

                del USERS_IN_MESSAGE_SEQUENCE[event.user_id]

                # TODO сделать сообщения в чат

            else:
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=create_keyboard("Ввести заявку заново", "Вернуться в меню").get_keyboard(),
                    message="Хотите ввести заявку заново или вернуться в главное меню?"
                )

                USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 3

        elif USERS_IN_MESSAGE_SEQUENCE[event.user_id] == 3:
            # TODO удалить последнюю запись этого пользователя
            if event.text == "Ввести заявку заново":
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    message="Введите вашу заявку в рамках одного сообщения. Приложите к этому сообщению все нужные "
                            "файлы"
                )

                USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 1

            else:
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=create_keyboard().get_keyboard(),
                    message='Выберите действие'
                )
                del USERS_IN_MESSAGE_SEQUENCE[event.user_id]

    else:
        vk.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=create_keyboard().get_keyboard(),
            message='Выберите действие'
        )


async def run_vk_bot(token: String) -> None:
    # создание сессии
    vk_session = VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    print(type(vk))

    # Основной цикл обработки событий
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            await message_reply(vk, event)


