
import sqlite3
from database.db import DB_PATH


STOP_WORDS = {
    "and", "the", "for", "with", "our", "you", "your",
    "are", "this", "that", "from", "have", "has", "need",
    "want", "looking", "please", "can", "will", "would",
    "who", "what", "how", "its", "their", "they"
}


ROLE_KEYWORDS = {
    "Automation Builder": {
        "automation", "workflow", "python", "api",
        "integration", "bot", "technical", "software"
    },
    "Outreach Strategist": {
        "outreach", "sales", "marketing", "customer",
        "communication", "business", "leads", "clients"
    },
    "Content Creator": {
        "content", "design", "graphic", "writing",
        "social", "video", "creative", "media"
    }
}


def get_words(text):

    return {
        word.strip(".,!?()[]{}:;\"'")
        for word in str(text or "").lower().split()
        if len(word.strip(".,!?()[]{}:;'")) > 2
        and word.strip(".,!?()[]{}:;'") not in STOP_WORDS
    }


def assign_best_intern(lead_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT needs, inquiry
        FROM leads
        WHERE id = ?
    """, (lead_id,))

    lead = cursor.fetchone()

    if not lead:
        conn.close()
        raise ValueError("Lead not found.")

    lead_text = f"{lead[0]} {lead[1]}"
    lead_words = get_words(lead_text)

    cursor.execute("""
        SELECT id, name, skills, background,
               interests, experience, assigned_role
        FROM intern_profiles
    """)

    interns = cursor.fetchall()
    conn.close()

    if not interns:
        raise ValueError("No intern profiles found.")

    if not lead_words:
        raise ValueError("Lead requirements are insufficient for matching.")

    best_intern = None
    best_score = 0
    best_reason = ""

    for intern in interns:

        intern_id, name, skills, background, interests, experience, role = intern

        profile_text = " ".join([
            str(skills or ""),
            str(background or ""),
            str(interests or ""),
            str(experience or "")
        ])

        profile_words = get_words(profile_text)

        skill_matches = lead_words.intersection(profile_words)

        role_words = ROLE_KEYWORDS.get(role, set())
        role_matches = lead_words.intersection(role_words)

        # Skill matches carry more weight than role matches.
        score = (
            len(skill_matches) * 10
            + len(role_matches) * 5
        )

        score = min(score, 100)

        if score > best_score:

            best_score = score
            best_intern = intern

            matching_keywords = sorted(skill_matches | role_matches)
            
            if skill_matches and role_matches:
                best_reason = (
                    f"The intern is a suitable match because their profile "
                    f"includes skills related to the client's requirements. "
                    f"Their assigned role as {role} also aligns with the "
                    f"type of work required."
                )
            
            elif skill_matches:
                best_reason = (
                    f"The intern is a relevant candidate because their "
                    f"profile includes skills that match the client's needs. "
                    f"These skills can help them handle the assigned task."
                )
            
            elif role_matches:
                best_reason = (
                    f"The intern's assigned role as {role} is relevant "
                    f"to the client's requirements, making them a suitable "
                    f"candidate for this task."
                )
            
            best_reason += (
                "\n\nMatching Keywords: "
                + ", ".join(matching_keywords)
            )

    if best_intern is None or best_score == 0:

        return {
            "matched": False,
            "message": (
                "No suitable intern found. "
                "No assignment has been made."
            )
        }

    return {
        "matched": True,
        "intern_id": best_intern[0],
        "intern_name": best_intern[1],
        "match_score": round(best_score, 2),
        "assignment_reason": best_reason
    }
