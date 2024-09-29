from config import *
from future.backports.datetime import datetime, timedelta
import mysql.connector


class BotDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
            connection_timeout=DB_CONNECTION_TIMEOUT
        )
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

    def connect(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        pass

    def get_last_hour_tenders(self):
        """Достаем сущности"""
        self.connect()
        date_to = datetime.now()
        date_from = (date_to - timedelta(hours=1)).strftime("%Y-%m-%d %H:00")
        date_to = date_to.strftime("%Y-%m-%d %H:00")
        print(date_from, date_to)
        sql = '''
            SELECT * 
            FROM `{table:s}` 
            WHERE 1 
                AND is_active = 1
                AND dt_start >= '{date_from:s}'
                AND dt_start < '{date_to:s}'
            ORDER BY dt_start ASC
        '''
        sql = sql.format(table=DB_TABLE_NAME, date_from=date_from, date_to=date_to)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.close()
        return result

    def close(self):
        """Закрываем соединение с БД"""
        if DB_RECONNECT_CONNECTION_AFTER_QUERY:
            self.conn.reconnect()
        pass
