from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_UA

btn_yes: KeyboardButton = KeyboardButton(text=LEXICON_UA['yes_button'])
btn_no: KeyboardButton = KeyboardButton(text=LEXICON_UA['no_button'])

yes_no_keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
yes_no_keyboard_builder.row(btn_yes, btn_no, width=2)
yes_no_kb = yes_no_keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

btn_rock: KeyboardButton = KeyboardButton(text=LEXICON_UA['rock'])
btn_paper: KeyboardButton = KeyboardButton(text=LEXICON_UA['paper'])
btn_scissors: KeyboardButton = KeyboardButton(text=LEXICON_UA['scissors'])

game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[btn_rock], [btn_scissors], [btn_paper]],
    resize_keyboard=True
)
