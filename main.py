import asyncio

import constants
from vk_bot.vk_bot import run_vk_bot

from web.web import run_web


# TODO здесь должен быть красивый запуск всех программ
async def main():
    await run_vk_bot(constants.vk_token)
    await run_web()

if __name__ == '__main__':
    asyncio.run(main())