from aiogram import executor

from dispatcher import dp
from config import *
from handlers import actions

if __name__ == "__main__":
    if ENV == "PROD":
        while True:
            try:
                executor.start_polling(dp)
            except Exception as e:
                print(e)
    else:
        executor.start_polling(dp)
    pass
