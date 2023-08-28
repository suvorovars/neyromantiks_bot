import asyncio

import constants
from vk_bot.vk_bot import run_vk_bot

if __name__ == '__main__':
    asyncio.run(run_vk_bot(constants.vk_token))