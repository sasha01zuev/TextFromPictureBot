from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from data.config import ADMINS_ID


from loader import dp, db, bot


@dp.message_handler(Command('get_user_info'), user_id=ADMINS_ID)
async def get_user_info(message: Message):
    try:
        user_id = int(message.get_args())
        _, username, first_name = await db.get_user(user_id)
        _, registration_date, lang_code = await db.get_user_info(user_id)
        answer = f'Имя: {first_name}\n' \
                 f'Username: {username}\n' \
                 f'Язык: {lang_code}\n\n' \
                 f'Платные подписки:\n'

        user_subscribes = await db.get_user_subscribes(user_id)
        if user_subscribes:
            for user_subscribe in user_subscribes:
                subscribe_id, _, donation_id, date_to = user_subscribe
                answer += f'ID: {subscribe_id}, Donation_id: {donation_id}, Подписка до: {date_to}\n'

        user_donations = await db.get_user_donations(user_id)
        answer += '\nДонаты:\n'
        if user_donations:
            for user_donate in user_donations:
                donation_id, _, amount, currency, donate_message, datetime = user_donate
                answer += f'ID: {donation_id}, Сумма: ${amount}, Валюта: {currency}, ' \
                          f'Сообщение: {donate_message}, Дата: {datetime}\n'

        try:
            profile_photo = await bot.get_user_profile_photos(user_id, limit=1)
            profile_photo = profile_photo['photos'][0][-1]['file_id']
            await message.answer_photo(profile_photo)
        except:
            pass

        await message.answer(answer)
    except ValueError:
        await message.answer('Не правильный user_id !')
    except Exception as err:
        await message.answer(f'Ошибка:\n{err}')


