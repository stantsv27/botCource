from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_UA

router: Router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_UA['other_answer'])
