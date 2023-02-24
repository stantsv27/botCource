from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon import LEXICON_UA
from services.services import get_bot_choice, get_winner


router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_UA['/start'], reply_markup=yes_no_kb)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_UA['/help'], reply_markup=yes_no_kb)


@router.message(Text(text=LEXICON_UA['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_UA['yes'], reply_markup=game_kb)


@router.message(Text(text=LEXICON_UA['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_UA['no'])


@router.message(Text(text=[LEXICON_UA['rock'],
                           LEXICON_UA['paper'],
                           LEXICON_UA['scissors']]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f"{LEXICON_UA['bot_choice']} "
                              f"- {LEXICON_UA[bot_choice]}")
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_UA[winner], reply_markup=yes_no_kb)
