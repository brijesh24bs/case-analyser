import sqlite3

# database class to handle all the database operations
class Database:
    def __init__(self):
        '''
        Initializes the connection and cursor to the database.
        '''
        self.connection = sqlite3.connect('cases.db')
        self.cursor = self.connection.cursor()
        
    
    def create_table(self):
        '''
        Creates the cases table if it does not exist.
        '''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                analysis TEXT NOT NULL
            )
        ''')
        self.connection.commit()
    
    def add_case(self, description, category, summary, analysis):
        '''
        Adds a new case to the database.
        '''
        self.cursor.execute('''
            INSERT INTO cases (description, category, summary, analysis)
            VALUES (?, ?, ?, ?)
        ''', (description, category, summary, analysis))
        self.connection.commit()
    
    def get_all_cases(self):
        self.cursor.execute('''
            SELECT * FROM cases
        ''')
        return self.cursor.fetchall()
    
    def delete_case(self, case_id):
        self.cursor.execute('''
            DELETE FROM cases WHERE id = ?
        ''', (case_id,))
        self.connection.commit()
    
    def __del__(self):
        self.connection.close()

# The Database class encapsulates all the database operations required for the case management system.

