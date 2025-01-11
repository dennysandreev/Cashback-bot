from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
import asyncio

# Bot Token
API_TOKEN = '8178674621:AAHrwgT7ZM9ackE7zll5fnvVKa62wanjt_M'

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher setup
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# User data storage (in-memory for simplicity)
user_data = {}

# Keyboards
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Добавить карту"),
              KeyboardButton("Посмотреть текущие категории кэшбэка"),
              KeyboardButton("Найти карту для покупки"))

default_back = ReplyKeyboardMarkup(resize_keyboard=True)
default_back.add(KeyboardButton("Вернуться в главное меню"))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"cards": {}}

    await message.reply(
        "Привет! Я помогу тебе выбрать карту с максимальным кэшбэком для твоих покупок. Что хочешь сделать?",
        reply_markup=main_menu
    )

@dp.message_handler(lambda message: message.text == "Добавить карту")
async def add_card(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["step"] = "add_card_name"
    await message.reply("Введите название банка и тип карты (например, Тинькофф Платинум):", reply_markup=default_back)

@dp.message_handler(lambda message: "step" in user_data.get(message.from_user.id, {}) and user_data[message.from_user.id]["step"] == "add_card_name")
async def add_card_name(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["current_card"] = {"name": message.text, "categories": []}
    user_data[user_id]["step"] = "add_card_categories"
    await message.reply("Какие категории у этой карты с повышенным кэшбэком? Перечислите через запятую или нажмите 'Обновить автоматически'.", reply_markup=default_back)

@dp.message_handler(lambda message: "step" in user_data.get(message.from_user.id, {}) and user_data[message.from_user.id]["step"] == "add_card_categories")
async def add_card_categories(message: types.Message):
    user_id = message.from_user.id
    categories = message.text.split(",")
    user_data[user_id]["current_card"]["categories"] = [cat.strip() for cat in categories]
    card = user_data[user_id]["current_card"]
    user_data[user_id]["cards"][card["name"]] = card
    user_data[user_id].pop("current_card", None)
    user_data[user_id].pop("step", None)
    await message.reply(f"Карта '{card['name']}' добавлена с категориями: {', '.join(card['categories'])}", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Посмотреть текущие категории кэшбэка")
async def view_categories(message: types.Message):
    user_id = message.from_user.id
    cards = user_data[user_id].get("cards", {})
    if not cards:
        await message.reply("У вас ещё нет добавленных карт. Нажмите 'Добавить карту'.", reply_markup=main_menu)
    else:
        reply = "Ваши карты и категории кэшбэка:\n"
        for card_name, details in cards.items():
            reply += f"{card_name}: {', '.join(details['categories'])}\n"
        await message.reply(reply, reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Найти карту для покупки")
async def find_card(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["step"] = "find_card"
    await message.reply("Что вы хотите купить? Опишите товар или услугу.", reply_markup=default_back)

@dp.message_handler(lambda message: "step" in user_data.get(message.from_user.id, {}) and user_data[message.from_user.id]["step"] == "find_card")
async def analyze_purchase(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id].pop("step", None)

    # Dummy NLP model to classify categories (replace with actual NLP logic)
    categories_map = {
        "электроника": ["колонка", "телевизор", "смартфон"],
        "одежда": ["пальто", "куртка", "джинсы"],
        "продукты": ["хлеб", "молоко", "сыр"]
    }

    user_input = message.text.lower()
    matched_category = None

    for category, keywords in categories_map.items():
        if any(keyword in user_input for keyword in keywords):
            matched_category = category
            break

    if not matched_category:
        await message.reply("Извините, я не смог определить категорию. Попробуйте описать покупку иначе.", reply_markup=main_menu)
        return

    # Recommend card
    cards = user_data[user_id].get("cards", {})
    best_card = None

    for card_name, details in cards.items():
        if matched_category in details["categories"]:
            best_card = card_name
            break

    if best_card:
        await message.reply(f"Рекомендую использовать карту '{best_card}' для категории '{matched_category}'.", reply_markup=main_menu)
    else:
        await message.reply("У вас нет карты с кэшбэком для этой категории.", reply_markup=main_menu)

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
