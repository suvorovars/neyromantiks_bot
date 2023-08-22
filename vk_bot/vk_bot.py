import random

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType


def get_token(filename):
    with open(filename) as f:
        token = f.read()
        if not token.startswith('vk'):
            raise ValueError('Invalid token')
        return token

# Создание клавиатуры
def create_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Просмотр заявок", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Подать заявку", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


# Ваш токен для доступа к API ВКонтакте
token = get_token('token.txt')

# Авторизация
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# Основной цикл обработки событий
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Отправка клавиатуры события и сообщения
        vk.messages.send(
            user_id=event.user_id,
            message="Выберите действие:",
            keyboard=create_keyboard(),
            random_id=random.getrandbits(31)  # Генерируем случайное значение для random_id
        )

        # Получаем текст сообщения
        message_text = event.text

        # Получаем ID пользователя, отправившего сообщение
        user_id = event.user_id

        # Обработка действий пользователя
        if message_text.lower() == "просмотр заявок":
            # Здесь будет код для вывода списка заявок
            pass
        elif message_text.lower() == "подать заявку":
            # Здесь будет код для начала процесса подачи заявки
            pass