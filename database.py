import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self.create_connection(db_name)
        self.create_table()

    @staticmethod
    def create_connection(db_name):
        try:
            conn = sqlite3.connect(db_name, check_same_thread=False)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Games (
                    name TEXT NOT NULL,
                    post_date TEXT,
                    info TEXT,
                    link TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_games(self, games):
        try:
            cursor = self.conn.cursor()

            game_data = [
                (game.name, game.post_date, game.info, game.link)
                for game in games
            ]

            cursor.executemany('''
                INSERT INTO Games (name, post_date, info, link)
                VALUES (?, ?, ?, ?)
            ''', game_data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding games: {e}")

    def get_game_by_name(self, game_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Games WHERE name = ?", (game_name,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving game: {e}")
            return None

    def delete_game(self, game_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Games WHERE name = ?", (game_name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting game: {e}")

    def clear_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Games")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table: {e}")

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    db = Database('PcGameTorrents.db')
    db.clear_table()
    db.close_connection()
