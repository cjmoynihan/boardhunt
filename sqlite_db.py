"""
This file keeps track of the scrapper information in the sqlite database
"""
# imports
import sqlite3 as sq3
from datetime import datetime

# constants
DB_NAME = 'boardhunt.db'
SCHEMA = 'boardhunt.sqlite'


class DB:
    def __init__(self):
        self.conn = sq3.connect(DB_NAME)
        self.c = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        with open(SCHEMA) as f:
            for command in '\n'.join(f.readlines()).split(';'):
                self.c.execute(command)
            self.conn.commit()

    def add_entry(self, user, game, rating):
        alt_action = "REPLACE" if rating else "IGNORE"
        self.c.execute(
            f"INSERT OR {alt_action} INTO bd_data (user, game, rating) VALUES (?, ?, ?)",
            (user, game, rating)
        )
        self.conn.commit()

    def get_entries_by_game(self, game):
        self.c.execute("""
            SELECT user, rating
            FROM bd_data
            WHERE game = ?
        """, (game,))
        return self.c.fetchall()

    def game_completed(self, game):
        game = game.lower()
        self.c.execute("""
            SELECT *
            FROM completed_games
            WHERE game = ?
        """, (game,))
        return len(self.c.fetchone())

    def mark_game_completed(self, game):
        game = game.lower()
        self.c.execute("""INSERT OR IGNORE INTO completed_games (game, date)
            VALUES (?, ?)""", (game, datetime.now()))
        self.conn.commit()
