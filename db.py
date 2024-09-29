import config
import mysql.connector

from config import DB_TABLE_NAME


class BotDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME,
            connection_timeout=config.DB_CONNECTION_TIMEOUT
        )
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

    def connect(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        pass

    def get_planned_tenders(self):
        """Достаем сущности"""
        self.connect()
        self.cursor.execute("SELECT * FROM " + DB_TABLE_NAME + " WHERE is_active = 1 ORDER BY id DESC")
        result = self.cursor.fetchall()
        self.close()
        return result

    def close(self):
        """Закрываем соединение с БД"""
        if config.DB_RECONNECT_CONNECTION_AFTER_QUERY:
            self.conn.reconnect()
        pass
