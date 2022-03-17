from aiogram import types
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import MAIN_ADMIN
from keyboards.inline import confirm_mass_mailing_keyboard
from loader import dp, db, bot


@dp.message_handler(Command('mass_mailing'), user_id=MAIN_ADMIN)
async def mass_mailing(message: types.Message, state: FSMContext):
    # /mass_mailing (Audience: [ru/en/uk/all]) (Photo: [true/false]) (First_button(Optional): [Button_name-link])
    # (Second_button(Optional): [Button_name-link]) (Third_button(Optional): [Button_name-link])
    args = message.get_args().split()
    args_quantity = len(args)

    if args_quantity == 1 or (1 < args_quantity <= 5 and args[1].lower() == 'false'):  # Text
        audience = args[0] if args[0] in ['ru', 'en', 'uk', 'all'] else 'ru'
        buttons_quantity = args_quantity - 2 if args_quantity > 2 else 0

        first_button = None
        second_button = None
        third_button = None

        if buttons_quantity == 1:
            first_button = args[2].split(sep='-')
        elif buttons_quantity == 2:
            first_button = args[2].split(sep='-')
            second_button = args[3].split(sep='-')
        elif buttons_quantity == 3:
            first_button = args[2].split(sep='-')
            second_button = args[3].split(sep='-')
            third_button = args[4].split(sep='-')

        await message.answer('Введите текст рассылки ниже 🠗 Форматирование текста - HTML')
        await state.set_state('ConfirmingTextMessage')
        await state.update_data(audience=audience, buttons_quantity=buttons_quantity, first_button=first_button,
                                second_button=second_button, third_button=third_button)
    elif 1 < args_quantity <= 5 and args[1].lower() == 'true':  # Photo + Text
        audience = args[0] if args[0] in ['ru', 'en', 'uk', 'all'] else 'ru'
        buttons_quantity = args_quantity - 2 if args_quantity > 2 else 0

        first_button = None
        second_button = None
        third_button = None

        if buttons_quantity == 1:
            first_button = args[2].split(sep='-')
        elif buttons_quantity == 2:
            first_button = args[2].split(sep='-')
            second_button = args[3].split(sep='-')
        elif buttons_quantity == 3:
            first_button = args[2].split(sep='-')
            second_button = args[3].split(sep='-')
            third_button = args[4].split(sep='-')

        await message.answer('Пришлите фото + описание ниже 🠗 Форматирование текста - HTML')
        await state.set_state('ConfirmingPhotoTextMessage')
        await state.update_data(audience=audience, buttons_quantity=buttons_quantity, first_button=first_button,
                                second_button=second_button, third_button=third_button)
    else:
        await message.answer('Ошибка!\n Следуй шаблону: /mass_mailing (Audience: [ru/en/uk/all]) (Photo: [true/false]) '
                             '(First_button(Optional): [Button_name-link]) (Second_button(Optional): '
                             '[Button_name-link]) (Third_button(Optional): [Button_name-link])')


@dp.message_handler(state="ConfirmingTextMessage")  # Text
async def confirming_text(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    buttons = (state_data['first_button'], state_data['second_button'], state_data['third_button'])
    message_text = message.text

    mass_mailing_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=' '.join(button[0].split(sep='_')), url=button[1])
            ] for button in buttons if button
        ]
    )

    await message.answer(f'{message_text}', reply_markup=mass_mailing_keyboard)
    await message.answer('Подтвердите сообщение выше 🠕', reply_markup=confirm_mass_mailing_keyboard)
    await state.update_data(keyboard=mass_mailing_keyboard, message_text=message_text)


@dp.message_handler(state='ConfirmingPhotoTextMessage')  # Photo + Text
async def confirming_photo_text(message: types.Message, state: FSMContext):
    await message.answer('Пришлите фотографию с описанием!')


@dp.message_handler(content_types=ContentType.PHOTO, state='ConfirmingPhotoTextMessage')  # Photo + Text
async def confirming_photo_text(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    buttons = (state_data['first_button'], state_data['second_button'], state_data['third_button'])
    photo_text = message.caption
    photo_id = message.photo[-1].file_id

    mass_mailing_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=' '.join(button[0].split(sep='_')), url=button[1])
            ] for button in buttons if button
        ]
    )

    await message.answer_photo(photo_id, photo_text, reply_markup=mass_mailing_keyboard)
    await message.answer('Подтвердите сообщение выше 🠕', reply_markup=confirm_mass_mailing_keyboard)
    await state.update_data(keyboard=mass_mailing_keyboard, message_text=photo_text, photo_id=photo_id)


@dp.callback_query_handler(text="confirm_mass_mailing", state="ConfirmingTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    state_data = await state.get_data()
    audience = state_data['audience']
    mass_mailing_keyboard = state_data['keyboard']
    message_text = state_data['message_text']

    users = await db.get_users_by_language(audience)

    sent = 0
    not_sent = 0

    if users:
        for user in users:
            try:
                await bot.send_message(chat_id=int(user['user_id']), text=f'{message_text}',
                                       reply_markup=mass_mailing_keyboard)
                sent = sent + 1
            except:
                not_sent = not_sent + 1

        await call.message.answer(f'Отправленно: {sent} сообщений\n'
                                  f'Не отправлено: {not_sent} сообщений')
    else:
        await call.message.answer(f'Нету пользователей с языком {audience}!')
    await state.finish()


@dp.callback_query_handler(text="confirm_mass_mailing", state="ConfirmingPhotoTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    state_data = await state.get_data()
    audience = state_data['audience']
    mass_mailing_keyboard = state_data['keyboard']
    message_text = state_data['message_text']
    photo_id = state_data['photo_id']

    users = await db.get_users_by_language(audience)

    sent = 0
    not_sent = 0

    if users:
        for user in users:
            try:
                await bot.send_photo(chat_id=int(user['user_id']), photo=photo_id,
                                     caption=f'{message_text if message_text else ""}',
                                     reply_markup=mass_mailing_keyboard)
                sent = sent + 1
            except:
                not_sent = not_sent + 1

        await call.message.answer(f'Отправленно: {sent} сообщений\n'
                                  f'Не отправлено: {not_sent} сообщений')
    else:
        await call.message.answer(f'Нету пользователей с языком {audience}!')
    await state.finish()
