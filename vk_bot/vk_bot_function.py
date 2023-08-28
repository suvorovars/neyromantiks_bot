from tokenize import String

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_token(filename) -> String:
    with open(filename) as f:
        token = f.read()
        if not token.startswith('vk'):
            raise ValueError('Invalid token')
        return token


def create_keyboard(*lst: String) -> VkKeyboard:
    keyboard = VkKeyboard(one_time=True)
    if not lst:
        keyboard.add_button('Подать заявку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Проверить состояние заявок', color=VkKeyboardColor.SECONDARY)
    else:
        for i in lst:
            keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
    return keyboard
