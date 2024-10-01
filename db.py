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
            SELECT 
                prof.public_email,
                prof.public_phone,
                prof.`name` user_name,
                t.id,
                t.`name` tender_name,
                p.name_full as project_name,
                p.address_object_name_capital_construction as project_address,
                IF (sc.kind_procedure_id = 1, 'Тендер', IF (sc.kind_procedure_id = 2, 'Аукцион', IF (sc.kind_procedure_id = 3, 'Запрос цены', ''))) as tender_type,
                t.contact_contract as contact,
                t.description_full as description,
                t.is_active,
                DATE_FORMAT(t.dt_end, '%d.%m.%Y') as until_date
            FROM
                `{table:s}` t
                    LEFT JOIN
                tender_scenario sc ON t.tender_scenario_id = sc.id
                    LEFT JOIN
                dict_project p ON p.id = t.project_id
                    LEFT JOIN
                user u ON u.id = t.responsible_user_id_first
                    LEFT JOIN
                profile prof ON prof.user_id = u.id
                    LEFT JOIN
                status st ON st.id = t.current_status_id
            WHERE 1 
                AND t.is_active = 1
                AND st.action_status_id = 2
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
