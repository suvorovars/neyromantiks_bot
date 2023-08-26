from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi

from vk_bot_function import *

def main():
    # создание сессии
    vk_session = VkApi(token=get_token("token.txt"))
    longpoll = VkLongPoll(vk_session)


    # Основной цикл обработки событий
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # Отправляем обратно полученное сообщение
            send_message(vk_session, event.user_id, event.text)


if __name__ == '__main__':
    main()