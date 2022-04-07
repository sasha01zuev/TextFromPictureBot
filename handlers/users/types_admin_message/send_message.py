from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from data.config import MAIN_ADMIN
from loader import dp, bot, _
from states import ConfirmMsgToAdmin


@dp.message_handler(state=ConfirmMsgToAdmin.SetMessageType)
async def send_message(message: Message, state: FSMContext):
    """Function for sending message to admin"""

    data = await state.get_data()
    message_type = data.get("type")
    await bot.send_message(MAIN_ADMIN, f'Тип сообщения: {message_type}\n'
                                       f'От: @{message.from_user.username}\n'
                                       f'ID: {message.from_user.id}\n'
                                       f'Сообщение:\n{message.text}')
    await message.answer(_('✅ Message sent successfully! Expect a response soon!'), reply_markup=ReplyKeyboardRemove())

    await state.finish()
