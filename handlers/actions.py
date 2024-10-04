from aiogram.utils.exceptions import *
from pyrogram import Client
from pyrogram.enums import ChatType

from config import *
from db import BotDB

db = BotDB()

client = Client(name='my_session', api_id=API_ID, api_hash=API_HASH)
client.start()

def main():
    if not before_action():
        return

    action_publish()

    if not after_action():
        return


def before_action():
    try:
        member = client.get_chat_member(CHAT_ALIAS, 'me')
        chat = client.get_chat(CHAT_ALIAS)
        if str(member.status) != 'ChatMemberStatus.ADMINISTRATOR':
            print('Member is not channel administrator')
            return False
        if chat.type == ChatType.CHANNEL:
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
        link = make_link(entity)
        f = open('template.html')
        caption = f.read()
        address = ''
        project = ''
        if entity['project_name']:
            project = ' по проекту ' + str(entity['project_name'])
        if entity['project_address']:
            address = ', по адресу ' + str(entity['project_address'])
        caption = caption.format(
            tender_name=str(link),
            tender_type=str(entity['tender_type']),
            user_name=str(entity['user_name']),
            project_name=project,
            address=address,
            tender_description=str(entity['description']),
            until_date=str(entity['until_date']),
            email=str(entity['public_email']),
            phone=str(entity['public_phone']),
        )
        photo = 'https://storage.yandexcloud.net/glorax-dev/c/p/p/di/56f1d27855aff51c0307a64917b737d408fb0f6b/9e296e03c7d40b64d4bace7bc8bd8dc9.jpg'
        client.send_photo(chat_id=CHAT_ALIAS, photo=photo, caption=caption)
        time.sleep(5)
    pass


def after_action():
    pass


def make_link(entity):
    if TMPL_LINK == "":
        return str(entity['tender_name'])
    url = TMPL_LINK + str(entity['id'])
    return '<a href="' + url + '">' + str(entity['tender_name']) + '</a>'
