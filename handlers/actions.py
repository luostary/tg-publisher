import os

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import *

from config import *
from db import BotDB
from dispatcher import dp, bot
from language import t

db = BotDB()

fileMessageIds = "message-ids.txt"


@dp.message_handler(commands=["start", "Back"], state='*')
async def start(message: types.Message):
    try:
        member = await bot.get_chat_member(CHAT_ALIAS, bot.id)
        if not member.is_chat_member():
            bot.send_message(message.from_user.id, t('The bot is not a member of group'))
            return
    except BaseException as e:
        print(str(e) + ' Необходимо добавить бота администратором канала с правами Post messages')
        return
    await start_menu(message)
    pass


@dp.callback_query_handler(lambda message: True, state='*')
async def inline_click(message):
    if message.data == 'delete_all':
        await delete_all()
    elif message.data == 'publish_list':
        await publish_list()


async def start_menu(message):
    markup = InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(t('Delete all'), callback_data='delete_all')
    item2 = InlineKeyboardButton(t('Publish list'), callback_data='publish_list')

    if message.from_user.id == ADMIN_ID:
        markup.add(item1).add(item2)
        await message.bot.send_message(message.from_user.id, t("Select command"), reply_markup=markup)


async def delete_all():
    if not exists(fileMessageIds):
        return
    f = open(fileMessageIds, "r")
    ids = f.read().split(',')
    for message_id in ids:
        try:
            await bot.delete_message(CHAT_ALIAS, message_id)
        except MessageToDeleteNotFound as e:
            print(str(e) + ': ' + message_id)
    if exists(fileMessageIds):
        os.remove(fileMessageIds)
    pass


async def publish_list():
    await delete_all()
    entities = db.get_planned_tenders()
    id_list = []
    for entity in entities:
        name = entity[TMPL_ENTITY_NAME]
        link = await make_link(entity)
        text = name + ' ' + link
        message = await bot.send_message(CHAT_ALIAS, text, parse_mode='HTML')
        time.sleep(1)
        id_list.append(message.message_id)
    id_string = ",".join(str(element) for element in id_list)
    await overwrite_file(id_string)
    pass


async def overwrite_file(ids):
    f = open(fileMessageIds, "a")
    f.write(ids)
    f.close()


async def markup_remove():
    return types.ReplyKeyboardRemove()


async def make_link(entity):
    if TMPL_LINK == "":
        return ''
    url = TMPL_LINK + '?' + TMPL_ENTITY_ID + '=' + str(entity[TMPL_ENTITY_ID])
    return '<a href="' + url + '">Перейти</a>'
