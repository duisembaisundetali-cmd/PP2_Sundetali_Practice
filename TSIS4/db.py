import psycopg2
from psycopg2 import sql
from datetime import datetime
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("Connected to PostgreSQL successfully")
        except Exception as e:
            print(f"Database connection error: {e}")
            print("Make sure PostgreSQL is running and database 'snake_game' exists")
    
    def create_tables(self):
        """Create tables if they don't exist"""
        try:
            with self.conn.cursor() as cur:
                # Create players table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    )
                """)
                
                # Create game_sessions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id SERIAL PRIMARY KEY,
                        player_id INTEGER REFERENCES players(id),
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                self.conn.commit()
                print("Tables created/verified successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    def get_or_create_player(self, username):
        """Get existing player ID or create new player"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                result = cur.fetchone()
                
                if result:
                    return result[0]
                else:
                    cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                    self.conn.commit()
                    return cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting/creating player: {e}")
            return None
    
    def save_game_result(self, username, score, level_reached):
        """Save game result to database"""
        try:
            player_id = self.get_or_create_player(username)
            if player_id:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO game_sessions (player_id, score, level_reached, played_at)
                        VALUES (%s, %s, %s, %s)
                    """, (player_id, score, level_reached, datetime.now()))
                    self.conn.commit()
                    print(f"Game result saved: {username} - Score: {score}")
                    return True
        except Exception as e:
            print(f"Error saving game result: {e}")
            return False
    
    def get_top_scores(self, limit=10):
        """Get top 10 all-time scores"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT p.username, gs.score, gs.level_reached, gs.played_at
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    ORDER BY gs.score DESC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
        except Exception as e:
            print(f"Error fetching top scores: {e}")
            return []
    
    def get_personal_best(self, username):
        """Get player's personal best score"""
        try:
            player_id = self.get_or_create_player(username)
            if player_id:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        SELECT MAX(score) as best_score
                        FROM game_sessions
                        WHERE player_id = %s
                    """, (player_id,))
                    result = cur.fetchone()
                    return result[0] if result and result[0] else 0
        except Exception as e:
            print(f"Error fetching personal best: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()