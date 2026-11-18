
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

def create_outreach_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_name TEXT,
            campaign TEXT,
            message TEXT,
            hook_score REAL,
            value_score REAL,
            cta_score REAL,
            overall_feedback TEXT,
            improved_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_outreach_attempt(intern_name, campaign, message, result):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO outreach_attempts (
            intern_name,
            campaign,
            message,
            hook_score,
            value_score,
            cta_score,
            overall_feedback,
            improved_version
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        intern_name,
        campaign,
        message,
        result["hook_score"],
        result["value_score"],
        result["cta_score"],
        result["overall_feedback"],
        result["improved_version"]
    ))

    conn.commit()
    conn.close()


def create_leads_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inquiry TEXT,
            email TEXT,
            budget TEXT,
            needs TEXT,
            timeline TEXT,
            urgency TEXT,
            lead_category TEXT,
            reasoning TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add email column to existing databases
    cursor.execute("PRAGMA table_info(leads)")
    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:
        cursor.execute(
            "ALTER TABLE leads ADD COLUMN email TEXT"
        )

    conn.commit()
    conn.close()


def normalize_text(value):
    return " ".join(str(value).casefold().split())


def is_duplicate_lead(email, inquiry):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT inquiry
        FROM leads
        WHERE LOWER(TRIM(email)) = ?
    """, (email.strip().lower(),))

    existing_inquiries = cursor.fetchall()
    conn.close()

    normalized_inquiry = normalize_text(inquiry)

    for row in existing_inquiries:
        if normalize_text(row[0]) == normalized_inquiry:
            return True

    return False


def save_lead(inquiry, result, email):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads (
            inquiry,
            email,
            budget,
            needs,
            timeline,
            urgency,
            lead_category,
            reasoning
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inquiry,
        email.strip().lower(),
        result["budget"],
        result["needs"],
        result["timeline"],
        result["urgency"],
        result["lead_category"],
        result["reasoning"]
    ))

    conn.commit()
    conn.close()


def create_task_assignments_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_assignment_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            intern_id INTEGER,
            match_score REAL,
            assignment_reason TEXT,
            status TEXT DEFAULT 'Assigned',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_task_assignment(lead_id, intern_id, match_score, assignment_reason):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO task_assignment_history (
            lead_id,
            intern_id,
            match_score,
            assignment_reason,
            status
        )
        VALUES (?, ?, ?, ?, 'Assigned')
    """, (
        lead_id,
        intern_id,
        match_score,
        assignment_reason
    ))

    conn.commit()
    conn.close()


def get_assignment_for_lead(lead_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT h.intern_id, i.name, h.match_score,
               h.assignment_reason, h.created_at
        FROM task_assignment_history h
        JOIN intern_profiles i ON h.intern_id = i.id
        WHERE h.lead_id = ?
        ORDER BY h.id DESC
        LIMIT 1
    """, (lead_id,))

    assignment = cursor.fetchone()
    conn.close()

    return assignment

def get_leads():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, needs, lead_category
        FROM leads
        ORDER BY id DESC
    """)

    leads = cursor.fetchall()
    conn.close()

    return leads

def get_interns():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, assigned_role, skills
        FROM intern_profiles
    """)

    interns = cursor.fetchall()
    conn.close()

    return interns

def get_assignment_history(lead_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.name,
            h.match_score,
            h.assignment_reason,
            h.status,
            h.created_at
        FROM task_assignment_history h
        JOIN intern_profiles i ON h.intern_id = i.id
        WHERE h.lead_id = ?
        ORDER BY h.id DESC
    """, (lead_id,))

    history = cursor.fetchall()
    conn.close()

    return history