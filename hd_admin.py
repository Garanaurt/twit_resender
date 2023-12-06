from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from typing import List
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
import uuid
from worker import gomain




router = Router()



@router.message(Command('start'))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    if chat_id > 0:
        await message.answer('Додай мене адміном на канал, можна вимкнути всі дозволи')



@router.channel_post(F.text)
async def any_message_answer(message: types.Message, bot: Bot):
    message = message.text
    gomain(message)



@router.channel_post(F.media_group_id)
async def process_product_photo(message: types.Message, bot: Bot, album: List[Message]):
    print('media group')
    post_text = ''
    file_paths = []
    for element in album:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        for k, v in caption_kwargs.items():
            if k == 'caption' and v is not None:
                post_text += v
        if element.photo:
            name = f'images/{uuid.uuid4()}.png'
            file_paths.append(str(name))
            input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
            await bot.download(input_media.media, destination=str(name))
        elif element.video:
            name = f'images/{uuid.uuid4()}{element.video.file_name[-4:]}'
            file_paths.append(str(name))
            input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs)
            try:
                await bot.download(input_media.media, destination=str(name))
            except TelegramBadRequest:
                pass
    print(post_text, file_paths, sep='\n')
    gomain(post_text, file_paths)
        


@router.channel_post(F.video)
@router.channel_post(F.photo)
async def process_product_one_photo(message: types.Message, bot: Bot):
    photo = ''
    file_paths = []
    if message.photo:
        file_paths = [f'images/{uuid.uuid4()}.png', ]
        photo = message.photo[-1].file_id
    elif message.video:
        file_paths = [f'images/{uuid.uuid4()}{message.video.file_name[-4:]}', ]
        photo = message.video.file_id
    if message.caption:
        post_text = message.caption
    else:
        post_text = ''   
    try:
        await bot.download(photo, destination=file_paths[0])
    except TelegramBadRequest:
        pass
    print(post_text, file_paths)
    gomain(post_text, file_paths)
    



#@router.message()
async def handle_messages(message: types.Message):
    print(message.text)