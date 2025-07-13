import sqlite3
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_file='data/db.sqlite'):
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date TIMESTAMP
        )
        ''')
        
        # Button clicks tracking
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS button_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            button_name TEXT,
            click_time TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        # Settings for welcome message and link
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        
        # Initialize default settings if they don't exist
        self.cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", 
                           ("welcome_text", "Welcome to our bot!"))
        self.cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", 
                           ("welcome_link", "https://example.com"))
        self.cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", 
                           ("welcome_link_text", "Visit our website"))
        
        self.connection.commit()
    
    def add_user(self, user_id, username=None, first_name=None, last_name=None):
        """Add new user to database or ignore if already exists"""
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, last_name, datetime.now())
        )
        self.connection.commit()
    
    def record_button_click(self, user_id, button_name):
        """Record when a user clicks a button"""
        self.cursor.execute(
            "INSERT INTO button_clicks (user_id, button_name, click_time) VALUES (?, ?, ?)",
            (user_id, button_name, datetime.now())
        )
        self.connection.commit()
    
    def get_user_stats(self, user_id):
        """Get statistics for a specific user"""
        self.cursor.execute(
            "SELECT button_name, COUNT(*) FROM button_clicks WHERE user_id = ? GROUP BY button_name",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def get_button_stats(self):
        """Get overall button click statistics"""
        self.cursor.execute(
            "SELECT button_name, COUNT(*) FROM button_clicks GROUP BY button_name ORDER BY COUNT(*) DESC"
        )
        return self.cursor.fetchall()
    
    def get_user_count(self):
        """Get total number of users"""
        self.cursor.execute("SELECT COUNT(*) FROM users")
        return self.cursor.fetchone()[0]
    
    def get_daily_stats(self, days=7):
        """Get daily statistics for the last N days"""
        result = []
        today = datetime.now().date()
        
        # Generate stats for each of the last N days
        for i in range(days):
            target_date = today - timedelta(days=i)
            start_date = datetime.combine(target_date, datetime.min.time())
            end_date = datetime.combine(target_date, datetime.max.time())
            
            self.cursor.execute(
                """
                SELECT COUNT(*) FROM button_clicks 
                WHERE click_time BETWEEN ? AND ?
                """,
                (start_date, end_date)
            )
            count = self.cursor.fetchone()[0]
            
            # Format as "DD.MM" (e.g., "01.05")
            date_str = target_date.strftime("%d.%m")
            result.append((date_str, count))
        
        # Return in chronological order (oldest first)
        return list(reversed(result))
    
    def get_most_active_users(self, limit=10):
        """Get the most active users based on button clicks"""
        self.cursor.execute(
            """
            SELECT u.user_id, u.username, u.first_name, u.last_name, COUNT(b.id) as click_count
            FROM users u
            JOIN button_clicks b ON u.user_id = b.user_id
            GROUP BY u.user_id
            ORDER BY click_count DESC
            LIMIT ?
            """,
            (limit,)
        )
        return self.cursor.fetchall()
    
    def get_active_users_count(self, days=7):
        """Get count of active users in the last N days"""
        target_date = datetime.now() - timedelta(days=days)
        
        self.cursor.execute(
            """
            SELECT COUNT(DISTINCT user_id) FROM button_clicks
            WHERE click_time >= ?
            """,
            (target_date,)
        )
        return self.cursor.fetchone()[0]
    
    # Settings methods
    def get_welcome_message(self):
        """Get welcome message text"""
        self.cursor.execute("SELECT value FROM settings WHERE key = 'welcome_text'")
        result = self.cursor.fetchone()
        return result[0] if result else "Welcome to our bot!"
    
    def get_welcome_link(self):
        """Get welcome link"""
        self.cursor.execute("SELECT value FROM settings WHERE key = 'welcome_link'")
        result = self.cursor.fetchone()
        return result[0] if result else "https://example.com"
    
    def get_welcome_link_text(self):
        """Get welcome link button text"""
        self.cursor.execute("SELECT value FROM settings WHERE key = 'welcome_link_text'")
        result = self.cursor.fetchone()
        return result[0] if result else "Visit our website"
    
    def update_setting(self, key, value):
        """Update a setting value"""
        self.cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
        self.connection.commit()
        return True
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close() 