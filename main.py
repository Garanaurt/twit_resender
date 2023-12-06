import asyncio
from aiogram import Bot, Dispatcher, BaseMiddleware
from typing import Any, Awaitable, Callable, Dict, List, Union
import hd_admin
from aiogram.types import (
    Message,
    TelegramObject,
)
from tokens import TOKEN






DEFAULT_DELAY = 0.6


class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.message.middleware(MediaGroupMiddleware())
    dp.channel_post.middleware(MediaGroupMiddleware())
    dp.include_routers(hd_admin.router)

    await bot.delete_webhook(drop_pending_updates=True)

    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())