ADMIN_ID = 0
BOT_TOKEN = ""
CHAT_ALIAS = "@YOUR_CHAT_NICKNAME"

DB_CONNECTION_TIMEOUT = 610
DB_HOST = "127.0.0.1"
DB_USER = "database_user"
DB_PASSWORD = "database_password"
DB_NAME = "database_name"
DB_TABLE_NAME = "table_name"
DB_RECONNECT_CONNECTION_AFTER_QUERY = True

ENV = "PROD"
TMPL_LINK = "https url to entity page"
TMPL_ENTITY_ID = 'id'
TMPL_ENTITY_NAME = 'name'

from os.path import exists

if exists('params.py'):
    from params import *
