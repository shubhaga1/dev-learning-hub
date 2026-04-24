"""
COMPONENT 1 — Data Store (simulates a database)

In production: PostgreSQL / BigQuery / DynamoDB
Here: plain Python dicts so you can see the shape clearly.

Three tables:
  USERS       — who our users are + their features
  POSTS       — content on the platform
  INTERACTIONS — historical likes/dislikes (training data)
"""

# ── Users ──────────────────────────────────────────────────
# Each user has a feature vector:
# [age_bucket, activity_level, tech_interest, sports_interest, news_interest]
USERS = {
    "u1": {"features": [0.2, 0.9, 0.9, 0.1, 0.2], "name": "Alice (tech lover)"},
    "u2": {"features": [0.6, 0.5, 0.1, 0.9, 0.3], "name": "Bob (sports fan)"},
    "u3": {"features": [0.4, 0.7, 0.5, 0.5, 0.8], "name": "Carol (news reader)"},
    "u4": {"features": [0.3, 0.8, 0.6, 0.4, 0.4], "name": "Dave (balanced)"},
}

# ── Posts ──────────────────────────────────────────────────
# Each post has metadata:
# [is_tech, is_sports, is_news, engagement_score, recency]
POSTS = {
    "p1":  {"features": [0.9, 0.0, 0.1, 0.8, 1.0], "title": "New AI breakthrough"},
    "p2":  {"features": [0.0, 0.9, 0.0, 0.7, 0.9], "title": "World Cup highlights"},
    "p3":  {"features": [0.1, 0.0, 0.9, 0.5, 0.8], "title": "Election results"},
    "p4":  {"features": [0.8, 0.1, 0.1, 0.6, 1.0], "title": "Python tips & tricks"},
    "p5":  {"features": [0.0, 0.8, 0.2, 0.9, 1.0], "title": "Viral sports moment"},
    "p6":  {"features": [0.7, 0.0, 0.3, 0.5, 0.7], "title": "Cloud computing guide"},
    "p7":  {"features": [0.1, 0.1, 0.8, 0.6, 0.9], "title": "Breaking news: economy"},
    "p8":  {"features": [0.0, 0.9, 0.1, 0.8, 1.0], "title": "Championship final"},
}

# ── Interactions (training data) ───────────────────────────
# (user_id, post_id, liked)
# 1 = liked/engaged, 0 = disliked/skipped
INTERACTIONS = [
    ("u1", "p1", 1), ("u1", "p2", 0), ("u1", "p4", 1), ("u1", "p3", 0),
    ("u1", "p6", 1), ("u1", "p5", 0), ("u1", "p7", 0), ("u1", "p8", 0),
    ("u2", "p2", 1), ("u2", "p5", 1), ("u2", "p8", 1), ("u2", "p1", 0),
    ("u2", "p3", 1), ("u2", "p4", 0), ("u2", "p6", 0), ("u2", "p7", 1),
    ("u3", "p3", 1), ("u3", "p7", 1), ("u3", "p1", 0), ("u3", "p2", 0),
    ("u3", "p5", 0), ("u3", "p4", 0), ("u3", "p6", 1), ("u3", "p8", 0),
    ("u4", "p1", 1), ("u4", "p2", 1), ("u4", "p3", 1), ("u4", "p4", 1),
    ("u4", "p5", 0), ("u4", "p6", 0), ("u4", "p7", 1), ("u4", "p8", 0),
]

# ── New posts arriving (simulates real-time stream) ────────
# These are posts that haven't been seen during training
NEW_POSTS = {
    "p9":  {"features": [0.9, 0.0, 0.1, 0.9, 1.0], "title": "GPT-5 released"},
    "p10": {"features": [0.0, 0.9, 0.0, 0.8, 1.0], "title": "Olympics opening ceremony"},
}

if __name__ == "__main__":
    print(f"Users:        {len(USERS)}")
    print(f"Posts:        {len(POSTS)}")
    print(f"Interactions: {len(INTERACTIONS)}")
    print(f"  Positive (liked):   {sum(1 for _,_,l in INTERACTIONS if l==1)}")
    print(f"  Negative (skipped): {sum(1 for _,_,l in INTERACTIONS if l==0)}")
    print(f"New posts (stream): {len(NEW_POSTS)}")
