
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "intern_profiles.db"


def create_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intern_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            education TEXT,
            background TEXT,
            skills TEXT,
            experience TEXT,
            interests TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_intern(name, email, education, background,
                skills, experience, interests):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO intern_profiles
        (name, email, education, background, skills, experience, interests)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        education,
        background,
        ", ".join(skills),
        experience,
        interests
    ))

    conn.commit()
    conn.close()
