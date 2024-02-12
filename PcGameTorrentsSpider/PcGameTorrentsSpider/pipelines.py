import os
import sqlite3
from itemadapter import ItemAdapter


class PcgametorrentsspiderPipeline:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath("C:/Users/deniz/PycharmProjects/PcGameTorrentsAPI/PcGameTorrents.db"))
        self.db_name = os.path.join(base_dir, 'PcGameTorrents.db')
        self.conn = self.create_connection(self.db_name)
        self.cursor = self.conn.cursor()
        self.open_spider(None)

    @staticmethod
    def create_connection(db_name):
        try:
            conn = sqlite3.connect(db_name, check_same_thread=False)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def open_spider(self, spider):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                post_date TEXT,
                info TEXT,
                link TEXT
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cursor.execute('''
            INSERT INTO Games (name, post_date, info, link) VALUES (?, ?, ?, ?)
        ''', (
            adapter.get('name'),
            adapter.get('post_date'),
            adapter.get('info'),
            adapter.get('link')
        ))
        self.conn.commit()

    def clear_table(self):
        try:
            self.cursor.execute("DELETE FROM Games")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table: {e}")

    def close_spider(self, spider):
        self.conn.close()


if __name__ == '__main__':
    db = PcgametorrentsspiderPipeline()
    db.clear_table()
    db.close_spider(None)
