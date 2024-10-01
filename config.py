API_HASH = ""
API_ID = 1
CHAT_ALIAS = "@YOUR_CHAT_NICKNAME"

DB_CONNECTION_TIMEOUT = 610
DB_HOST = "127.0.0.1"
DB_USER = "database_user"
DB_PASSWORD = "database_password"
DB_NAME = "database_name"
DB_TABLE_NAME = "table_name"
DB_RECONNECT_CONNECTION_AFTER_QUERY = True

TMPL_LINK = "https://example.com/path/view?id="

from os.path import exists

if exists('params.py'):
    from params import *
