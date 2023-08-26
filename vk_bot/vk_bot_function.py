# функция получения токена из файла
from tokenize import String

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_token(filename) -> String:
    with open(filename) as f:
        token = f.read()
        if not token.startswith('vk'):
            raise ValueError('Invalid token')
        return token


# функция отправки сообщения
def send_message(session, user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


def create_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Кнопка 1', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Кнопка 2', color=VkKeyboardColor.PRIMARY)
