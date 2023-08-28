import asyncio

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi
from vk_api.utils import get_random_id

from db.tasks import Task
from vk_bot.vk_bot_function import *

from db import db_session

import constants

db_session.global_init(constants.db_location)

USERS_IN_MESSAGE_SEQUENCE = {}


async def message_reply(vk, event):
    global USERS_IN_MESSAGE_SEQUENCE
    if event.text == 'Подать заявку':
        USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 1
        vk.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            message="Введите вашу заявку в рамках одного сообщения. Приложите к этому сообщению все нужные файлы "
        )
    elif event.text == "Проверить состояние заявок":
        session = db_session.create_session()
        tasks = session.query(Task).filter(Task.user_id == event.user_id)
        print(tasks)
        """
        Реализовать Вывод Задач
        """

    elif event.user_id in USERS_IN_MESSAGE_SEQUENCE.keys():
        if USERS_IN_MESSAGE_SEQUENCE[event.user_id] == 1:
            session = db_session.create_session()
            task = Task()
            task.user_id = event.user_id
            task.task = event.text
            task.files = '' # TODO здесь нужно закинуть ссылки на файлы
            session.add(task)

            vk.messages.send(
                peer_id=event.user_id,
                random_id=get_random_id(),
                keyboard=create_keyboard('Да', "Нет").get_keyboard(),
                message='Это всё, идём дальше?'
            )
            USERS_IN_MESSAGE_SEQUENCE[event.user_id] = 2
        elif USERS_IN_MESSAGE_SEQUENCE[event.user_id] == 2:
            if event.text.lower == "да":
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=create_keyboard().get_keyboard(),
                    message="Ваша заявка принята в обработку, ожидайте ответа администратора"
                )
                del USERS_IN_MESSAGE_SEQUENCE[event.user_id]
            else:
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=create_keyboard().get_keyboard(),
                    message=""
                )

    else:
        vk.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=create_keyboard().get_keyboard(),
            message='Выберите действие'
        )

async def run_vk_bot(token: String):
    # создание сессии
    vk_session = VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    # Основной цикл обработки событий
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            await message_reply(vk, event)


