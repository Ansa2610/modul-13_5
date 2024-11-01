from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton(text='Information')
button_count = KeyboardButton(text="Count")
kb.add(button_info)
kb.add(button_count)


class UserState(StatesGroup):
	age = State()
	growth = State()
	weight = State()


@dp.message_handler(text=['hello'])
async def hello_message(message):
	print('Enter command /start to initiate communication')
	await message.answer('Enter command /start to initiate communication')


@dp.message_handler(commands=['start'])
async def start(message):
	# print('Hello! I am bot and can count calories for women')
	await message.answer('Hello! I am bot and can count calories for women', reply_markup=kb)


@dp.message_handler(text='Count')
async def set_age(message):
	await message.answer(f'Enter your age')
	await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
	await state.update_data(age=message.text)
	await message.answer(f'Enter your growth in sm')
	await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
	await state.update_data(growth=message.text)
	await message.answer(f'Enter your weight in kg')
	await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
	await state.update_data(weight=message.text)
	data = await state.get_data()
	results = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
	await message.answer(f'Your normal amount of calories per day is {results}')
	await state.finish()


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
