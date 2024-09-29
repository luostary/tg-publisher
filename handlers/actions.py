from aiogram.utils.exceptions import *
from pyrogram import Client

from config import *
from db import BotDB

db = BotDB()


def main():
    if not before_action():
        return

    action_publish()

    if not after_action():
        return


def before_action():
    client = Client(name='my_session', api_id=API_ID, api_hash=API_HASH)
    client.start()
    try:
        member = client.get_chat_member(CHAT_ALIAS, 'me')
        if str(member.status) != 'ChatMemberStatus.ADMINISTRATOR':
            print('Member is not channel administrator')
            return False
        if not member.privileges.can_post_messages:
            print('Administrator has not permission can_post_messages')
            return False
        return True
    except BaseException as e:
        print(str(e))
        return False


def action_publish():
    entities = db.get_last_hour_tenders()
    for entity in entities:
        name = entity[TMPL_ENTITY_NAME]
        link = make_link(entity)
        text = name + ' ' + link
        print(text)
        # await bot.send_message(CHAT_ALIAS, text, parse_mode='HTML')
        time.sleep(2)
    pass


def after_action():
    pass


def make_link(entity):
    if TMPL_LINK == "":
        return ''
    url = TMPL_LINK + '?' + TMPL_ENTITY_ID + '=' + str(entity[TMPL_ENTITY_ID])
    return '<a href="' + url + '">Перейти</a>'
