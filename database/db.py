
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
            interests TEXT,
            assigned_role TEXT,
            assessment TEXT
        )
    """)

    # Update existing database if columns are missing
    cursor.execute("PRAGMA table_info(intern_profiles)")
    columns = [row[1] for row in cursor.fetchall()]

    if "assigned_role" not in columns:
        cursor.execute(
            "ALTER TABLE intern_profiles ADD COLUMN assigned_role TEXT"
        )

    if "assessment" not in columns:
        cursor.execute(
            "ALTER TABLE intern_profiles ADD COLUMN assessment TEXT"
        )

    conn.commit()
    conn.close()


def save_intern(name, email, education, background,
                skills, experience, interests,
                assigned_role=None, assessment=None):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO intern_profiles
        (name, email, education, background, skills,
         experience, interests, assigned_role, assessment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        education,
        background,
        ", ".join(skills),
        experience,
        interests,
        assigned_role,
        assessment
    ))

    conn.commit()
    conn.close()
