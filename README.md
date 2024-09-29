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
Копируем: ```config-example.py``` в файл ```config.py```
~~~
cp config-example.py config.py
~~~
