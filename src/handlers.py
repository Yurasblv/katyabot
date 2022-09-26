from aiogram import Dispatcher
from src.bot import bot, logger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.states import Person
from aiogram.dispatcher import FSMContext
from typing import Mapping, Optional
from src.config import Cfg
from aiogram import types


async def zero_handler(message: types.Message, state: FSMContext):
    logger.info(await state.get_data())
    btn1 = InlineKeyboardButton("Заполнить ✍", callback_data="Заполнить")
    kb1 = InlineKeyboardMarkup(row_width=2).add(btn1)
    await Person.ACCEPT.set()
    await bot.send_message(
        message.from_user.id,
        text="Привет🥰Рада,что ты решила изменить свою жизнь вместе со мной!❤\n"
             "Я составлю тебе программу на месяц, которая поможет тебе прийти к цели 🎯\n"
             "Для того,чтобы составить план действий , заполни пожалуйста анкету❤",
        reply_markup=kb1,
    )


async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(callback_query.data)
    async with state.proxy() as data:
        data["ACCEPT"] = True
    await Person.next()
    await bot.send_message(
        callback_query.from_user.id, text="Имя и фамилия:\n(через пробел)"
    )


async def name_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    print(message.from_user.id)
    async with state.proxy() as data:
        data["PERSON_CREDS"] = message.text
        print(data)
    await Person.next()
    await bot.send_message(message.from_user.id, text="Возраст\n(число)")


async def process_digit_name_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Число в имени или фамилии!")


async def process_wrong_name_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Неправильно указан формат")


async def age_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["AGE"] = message.text
    await Person.next()
    await bot.send_message(message.chat.id, text="Рост\n(в см)")


async def process_age_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Неправильно указан возраст")


async def height_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["HEIGHT"] = message.text
    await Person.next()
    await bot.send_message(message.chat.id, text="Вес\n(в кг)")


async def process_height_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Неправильно указан рост")


async def weight_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["WEIGHT"] = message.text
    await Person.next()
    inline_btn_1 = InlineKeyboardButton("Похудение", callback_data="Похудение")
    inline_btn_2 = InlineKeyboardButton(
        "Поддержание формы", callback_data="Поддержание формы"
    )
    inline_btn_3 = InlineKeyboardButton("Набор массы", callback_data="Набор массы")
    inline_kb1 = InlineKeyboardMarkup().add(
        inline_btn_1).add(inline_btn_2).add(inline_btn_3)
    await bot.send_message(
        message.chat.id, text="Какой план тренировок?", reply_markup=inline_kb1
    )


async def process_weight_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Неправильный указан возраст")


async def goal_handler(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(callback_query.data)
    async with state.proxy() as data:
        data["GOAL"] = callback_query.data
    await Person.next()
    inline_btn_1 = InlineKeyboardButton("🏟️ Зал", callback_data="Зал")
    inline_btn_2 = InlineKeyboardButton("🏠 Дома", callback_data="Дома")
    inline_kb1 = InlineKeyboardMarkup(row_width=3).row(inline_btn_1, inline_btn_2)
    await bot.send_message(callback_query.from_user.id, text=f"{data['GOAL']}")
    await bot.send_message(
        callback_query.from_user.id,
        text="Где будешь тренироваться?",
        reply_markup=inline_kb1,
    )


async def location_handler(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(callback_query.data)
    async with state.proxy() as data:
        data["LOCATION"] = callback_query.data
    if data["LOCATION"] == "Дома":
        inline_btn_1 = InlineKeyboardButton("✅ Да", callback_data="Да")
        inline_btn_2 = InlineKeyboardButton("❌ Нет", callback_data="Нет")
        inline_kb1 = InlineKeyboardMarkup(row_width=2).row(inline_btn_1, inline_btn_2)
        await Person.next()
        print(await state.get_state())
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['LOCATION']}"
        )
        await bot.send_message(
            callback_query.from_user.id,
            text="Есть ли у тебя инвентарь для занятий?",
            reply_markup=inline_kb1,
        )
    if data["LOCATION"] == "Зал":
        await state.update_data({"EQUIPMENT_BOOLEAN": "-", "EQUIPMENT_INFO": "-"})
        await Person.CONTRAINDICATIONS_BOOLEAN.set()
        inline_btn_1 = InlineKeyboardButton("✅ Да", callback_data="Да")
        inline_btn_2 = InlineKeyboardButton("❌ Нет", callback_data="Нет")
        inline_kb1 = InlineKeyboardMarkup(row_width=2).row(inline_btn_1, inline_btn_2)
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['LOCATION']}"
        )
        await bot.send_message(
            callback_query.from_user.id,
            text="Имеются ли противопоказания?",
            reply_markup=inline_kb1,
        )


async def equipment_bool_handler(
        callback_query: types.CallbackQuery, state: FSMContext
):
    logger.info(callback_query.data)
    async with state.proxy() as data:
        data["EQUIPMENT_BOOLEAN"] = callback_query.data
    if data["EQUIPMENT_BOOLEAN"] == "Да":
        await Person.next()
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['EQUIPMENT_BOOLEAN']}"
        )
        await bot.send_message(
            callback_query.from_user.id, text="Напиши какой есть в наличии"
        )
    if data["EQUIPMENT_BOOLEAN"] == "Нет":
        await state.update_data({"EQUIPMENT_INFO": "-"})
        await Person.CONTRAINDICATIONS_BOOLEAN.set()
        inline_btn_1 = InlineKeyboardButton("✅ Да", callback_data="Да")
        inline_btn_2 = InlineKeyboardButton("❌ Нет", callback_data="Нет")
        inline_kb1 = InlineKeyboardMarkup(row_width=2).row(inline_btn_1, inline_btn_2)
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['EQUIPMENT_BOOLEAN']}"
        )
        await bot.send_message(
            callback_query.from_user.id,
            text="Имеются ли противопоказания?",
            reply_markup=inline_kb1,
        )


async def equipment_info_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["EQUIPMENT_INFO"] = message.text
    await Person.next()
    inline_btn_1 = InlineKeyboardButton("✅ Да", callback_data="Да")
    inline_btn_2 = InlineKeyboardButton("❌ Нет", callback_data="Нет")
    inline_kb1 = InlineKeyboardMarkup(row_width=2).row(inline_btn_1, inline_btn_2)
    await bot.send_message(
        message.chat.id, text="Имеются ли противопоказания?", reply_markup=inline_kb1
    )


async def contraindications_handler_boolean(
        callback_query: types.CallbackQuery, state: FSMContext
):
    logger.info(callback_query.data)
    async with state.proxy() as data:
        data["CONTRAINDICATIONS_BOOLEAN"] = callback_query.data
    if data["CONTRAINDICATIONS_BOOLEAN"] == "Да":
        await Person.next()
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['CONTRAINDICATIONS_BOOLEAN']}"
        )
        await bot.send_message(callback_query.from_user.id, text="Опиши какие")
    if data["CONTRAINDICATIONS_BOOLEAN"] == "Нет":
        await state.update_data(
            {
                "CONTRAINDICATIONS_BOOLEAN": callback_query.data,
                "CONTRAINDICATIONS_INFO": "-",
            }
        )
        await Person.BREAST_SIZE.set()
        await bot.send_message(
            callback_query.from_user.id, text=f"{data['CONTRAINDICATIONS_BOOLEAN']}"
        )
        await bot.send_message(
            callback_query.from_user.id,
            text="Теперь необходима информация о твоих параметрах тела 🤩",
        )
        await bot.send_message(
            callback_query.from_user.id, text="Окружность груди\n(в см)"
        )


async def contraindications_handler_info(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["CONTRAINDICATIONS_INFO"] = message.text
    await Person.next()
    await bot.send_message(
        message.chat.id, text="Теперь необходима информация о твоих параметрах тела 🤩"
    )
    await bot.send_message(message.chat.id, text="Окружность груди\n(в см)")


async def process_breast_param_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Только числа!")


async def breast_param_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["BREAST_SIZE"] = message.text
    await Person.next()
    await bot.send_message(message.chat.id, text="Окружность талии\n(в см)")


async def process_waist_param_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Только числа!")


async def waist_param_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["WAIST_SIZE"] = message.text
    await Person.next()
    await bot.send_message(message.chat.id, text="Окружность бедер\n(в см)")


async def process_hips_param_invalid(message: types.Message):
    logger.info(message.text)
    return await message.reply("Только числа!")


async def hips_param_handler(message: types.Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        data["HIPS_SIZE"] = message.text
    inline_btn_1 = InlineKeyboardButton(text="Проверить", callback_data="Проверить")
    inline_kb_1 = InlineKeyboardMarkup().add(inline_btn_1)
    await bot.send_message(
        message.chat.id,
        text="Готово 😃\nТеперь проверь свои данные",
        reply_markup=inline_kb_1,
    )


async def check_info_handler(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(callback_query.data)
    inline_btn_1 = InlineKeyboardButton(text="Создать заново 🔙", callback_data="Заново")
    inline_btn_2 = InlineKeyboardButton(text="Отправить 📨", callback_data="Отправить")
    inline_kb_1 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
    await bot.send_message(
        callback_query.from_user.id,
        text=f"{await info_editor(data=await state.get_data())}\n"
             f" Если все правильно нажми \"Отправить\""
             f" если неправильно указана информация заполни снова нажав \"Создать заново\"",
        reply_markup=inline_kb_1,
    )


async def send_info_handler(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(callback_query.data)
    await bot.send_message(
        Cfg.CHANNEL_ID, text=await info_editor(data=await state.get_data())
    )
    await bot.send_message(
        callback_query.from_user.id,
        text="Я получила твою анкету🥳\nЖди программу 🧘‍♀\nЧтобы создать новое нажми в меню кнопку \"Перезагрузить 🔄\""
    )
    await state.reset_state()


async def rollback_info_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    callback_query.data = 'Заполнить'
    await Person.ACCEPT.set()
    await start_handler(callback_query, state)


async def info_editor(data: Optional[Mapping]):
    person_info = (
        f"ФИО: {data['PERSON_CREDS']}\n"
        f"Возраст: {data['AGE']}\n"
        f"Рост: {data['HEIGHT']}\n"
        f"Вес: {data['WEIGHT']}\n"
        f"Цель тренировок: {data['GOAL']}\n"
        f"Место занятий: {data['LOCATION']}\n"
        f"Наличие инвентаря: {data['EQUIPMENT_BOOLEAN']}\n"
        f"Какой инвентарь в наличии: {data['EQUIPMENT_INFO']}\n"
        f"Есть ли противопоказания: {data['CONTRAINDICATIONS_BOOLEAN']}\n"
        f"Какие имеются противопоказания: {data['CONTRAINDICATIONS_INFO']}\n"
        f"Замеры тела \n"
        f"- Обхват груди: {data['BREAST_SIZE']} см \n"
        f"- Обхват талии: {data['WAIST_SIZE']} см \n"
        f"- Обхват бедер: {data['HIPS_SIZE']} см \n"
    )
    return person_info


def register_handler(dp: Dispatcher):
    dp.register_message_handler(zero_handler, commands=["start", "reload"], state="*")
    dp.register_callback_query_handler(
        start_handler,
        lambda callback_query: callback_query.data == "Заполнить",
        state=Person.ACCEPT,
    )
    dp.register_message_handler(
        process_digit_name_invalid,
        lambda message: [message for char in message.text if char.isdigit()],
        state=Person.PERSON_CREDS,
    )
    dp.register_message_handler(
        process_wrong_name_invalid,
        lambda message: len(message.text.split()) != 2,
        state=Person.PERSON_CREDS,
    )
    dp.register_message_handler(
        name_handler,
        state=Person.PERSON_CREDS,
        regexp=r"^[A-Za-zА-Яа-яЁё]* [A-Za-zА-Яа-яЁё]+",
    )
    dp.register_message_handler(
        process_age_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.AGE,
    )
    dp.register_message_handler(age_handler, state=Person.AGE)
    dp.register_message_handler(
        process_height_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.HEIGHT,
    )
    dp.register_message_handler(height_handler, state=Person.HEIGHT)
    dp.register_message_handler(
        process_weight_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.WEIGHT,
    )
    dp.register_message_handler(weight_handler, state=Person.WEIGHT)
    dp.register_callback_query_handler(
        goal_handler,
        lambda callback_query: callback_query.data in ["Похудение",
                                                       "Поддержание формы",
                                                       "Набор массы"],
        state=Person.GOAL,
    )
    dp.register_callback_query_handler(
        location_handler,
        lambda callback_query: callback_query.data in ["Зал", "Дома"],
        state=Person.LOCATION,
    )
    dp.register_callback_query_handler(
        equipment_bool_handler,
        lambda callback_query: callback_query.data in ["Да", "Нет"],
        state=Person.EQUIPMENT_BOOLEAN,
    )
    dp.register_message_handler(equipment_info_handler, state=Person.EQUIPMENT_INFO)
    dp.register_callback_query_handler(
        contraindications_handler_boolean,
        lambda callback_query: callback_query.data in ["Да", "Нет"],
        state=Person.CONTRAINDICATIONS_BOOLEAN,
    )
    dp.register_message_handler(
        contraindications_handler_info, state=Person.CONTRAINDICATIONS_INFO
    )
    dp.register_message_handler(
        process_breast_param_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.BREAST_SIZE,
    )
    dp.register_message_handler(breast_param_handler, state=Person.BREAST_SIZE)
    dp.register_message_handler(
        process_waist_param_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.WAIST_SIZE,
    )
    dp.register_message_handler(waist_param_handler, state=Person.WAIST_SIZE)
    dp.register_message_handler(
        process_hips_param_invalid,
        lambda message: [message for char in message.text if not char.isdigit()],
        state=Person.HIPS_SIZE,
    )
    dp.register_message_handler(hips_param_handler, state=Person.HIPS_SIZE)
    dp.register_callback_query_handler(
        check_info_handler,
        lambda callback_query: callback_query.data == "Проверить",
        state=Person.HIPS_SIZE,
    )
    dp.register_callback_query_handler(
        send_info_handler,
        lambda callback_query: callback_query.data == "Отправить",
        state=Person.HIPS_SIZE,
    )
    dp.register_callback_query_handler(
        rollback_info_handler,
        lambda callback_query: callback_query.data == "Заново",
        state=Person.HIPS_SIZE,
    )
