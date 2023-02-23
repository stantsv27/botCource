from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import Message
from environs import Env
import random


env = Env()
env.read_env()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота
API_TOKEN: str = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 5

users: dict = {}


def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(
        'Привіт!\nДавай зіграємо в гру "Вгадай число?"\n\n'
        'Щоб отримати правила гри і список доступних команд - відправ команду\n/help'
        )
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила гри:\n\nЯ загадую число від 1 до 100, '
        f'а тобі потрібно його вгадати\nУ тебе є {ATTEMPTS}'
        f'спроб\n\nДоступні команди:\n/help - правила '
        f'гри і список команд\n/cancel - вийти з гри\n'
        f'/stat - подивитись статистику\n\nДавай зіграємо?'
        )


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(
        f"Всього ігор зіграно: {users[message.from_user.id]['total_games']}\n"
        f"Ігор виграно: {users[message.from_user.id]['wins']}\n"
        )


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Ви вийшли з гри. Якщо хочете зіграти '
            'знову - напишіть про це'
        )
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer(
            'А ми й так з вами не граємо.'
            'Може зіграємо разочок?'
        )


@dp.message(Text(text=['Так', "Давай", "Зіграємо", "Гра",
                       "Хочу грати", "Грати"], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Круто!\n\nЯ загадав число від 1 до 100, '
            'спробуй вгадати!'
        )
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attemts'] = ATTEMPTS
    else:
        await message.answer(
            'Поки ми граємо в гру я можу '
            'реагувати тільки на числа від 1 до 100 '
            'і команди /cancel і /stat'
        )


@dp.message(Text(text=['Ні', "Нє", "Не хочу", "Не буду"], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Шкода :(\n\nЯкщо захочеш зіграти - просто '
            'напиши мені про це'
        )
    else:
        await message.answer(
            'Ми ж зараз з тобою граємо. Надішли, '
            'будь ласка, число від 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer(
                'Вітаю!!! Ти вгадав число!\n\n'
                'Може зіграємо ще?'
                )
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Моє число менше')
            users[message.from_user.id]['attemts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Моє число більше')
            users[message.from_user.id]['attemts'] -= 1

        if users[message.from_user.id]['attemts'] == 0:
            await message.answer(
                'Нажаль в тебе більше не залишилось '
                'спроб. Ти програв =(\n\nМоє число '
                f'було {users[message.from_user.id]["secret_number"]}\n\n'
                'Давай зіграємо ще?'
            )
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Ми ще не граємо. Хочеш зіграти?')


dp.message()
async def process_other_text_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Ми ж зараз граємо. '
            'Надсилай числа від 1 до 100'
        )
    else:
        await message.answer(
            'Я достатньо обмежений бот. Давай '
            'просто зіграємо в гру?'
        )

if __name__ == '__main__':
    dp.run_polling(bot)
