Публикатор в Telegram канал
-
Инструкция для ОС Ubuntu

Менеджер пакетов
-
python3-pip

~~~
sudo apt-get install pip
~~~

Библиотеки
-

aiogram

~~~
pip install aiogram
~~~

Переходим в папку проекта
-

~~~
cd /var/www/myNewProjectForder
~~~

Клонирование проекта
-

~~~
git clone http://gitlab.alfa2b.ru/TENDER/tg-publisher.git ./
~~~

Дамп базы данных
-

Не требуется

Настраиваем локальный конфиг в корне
-
Название: ```params.py```

Пример содержимого:

~~~
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
TMPL_LINK = "https://domain.com/path/view"
TMPL_ENTITY_ID = 'id'
TMPL_ENTITY_NAME = 'name'
~~~