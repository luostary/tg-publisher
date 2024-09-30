from aiogram.utils.exceptions import *
from pyrogram import Client
from setuptools.package_index import entity_sub

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
            contact_name=str(entity['contact']),
            project_name=project,
            address=address,
            tender_description=str(entity['description']),
            until_date=str(entity['until_date'])
        )
        photo2 = 'cat100500.jpeg'
        client.send_photo(chat_id=CHAT_ALIAS, photo=photo2, caption=caption)
        time.sleep(5)
    pass


def after_action():
    pass


def make_link(entity):
    if TMPL_LINK == "":
        return ''
    url = TMPL_LINK + '?' + TMPL_ENTITY_ID + '=' + str(entity[TMPL_ENTITY_ID])
    return '<a href="' + url + '">' + str(entity[TMPL_ENTITY_NAME]) + '</a>'
