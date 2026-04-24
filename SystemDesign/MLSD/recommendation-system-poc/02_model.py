"""
COMPONENT 2 — ML Model

Turns user + post features into P(user likes post).

In production: PyTorch two-tower model or XGBoost
Here: Logistic Regression (same idea, simpler to follow)

Key concept: combine user features + post features + cross features
→ cross features capture "this user type likes this content type"
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from recsys_data import USERS, POSTS, INTERACTIONS


def make_features(user_id: str, post_id: str) -> list[float]:
    """
    Build one feature vector for a (user, post) pair.

    user features:  [age, activity, tech_interest, sports_interest, news_interest]
    post features:  [is_tech, is_sports, is_news, engagement, recency]
    cross features: user_interest × post_type  ← key interaction signals
    """
    u = USERS[user_id]["features"]
    p = POSTS[post_id]["features"]

    cross = [
        u[2] * p[0],   # tech_interest   × is_tech
        u[3] * p[1],   # sports_interest × is_sports
        u[4] * p[2],   # news_interest   × is_news
        u[1] * p[3],   # activity_level  × engagement_score
    ]
    return u + p + cross


def build_dataset(interactions: list) -> tuple:
    """Convert interaction log → X (features), y (labels)."""
    X, y = [], []
    for user_id, post_id, liked in interactions:
        X.append(make_features(user_id, post_id))
        y.append(liked)
    return np.array(X), np.array(y)


class RecommendationModel:
    """Wraps sklearn model with fit / predict / score helpers."""

    def __init__(self):
        self.model  = LogisticRegression(max_iter=500, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False

    def fit(self, interactions: list):
        X, y = build_dataset(interactions)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.trained = True
        auc = roc_auc_score(y, self.model.predict_proba(X_scaled)[:, 1])
        print(f"  Trained on {len(interactions)} interactions | AUC = {auc:.3f}")

    def partial_fit(self, new_interactions: list):
        """
        Incremental training — update model with new data only.
        In production: warm-start from existing weights or use online learning.
        Here: retrain on new batch (simplified).
        """
        if not self.trained:
            raise RuntimeError("Call fit() first before partial_fit()")
        X, y = build_dataset(new_interactions)
        X_scaled = self.scaler.transform(X)   # use existing scaler
        self.model.fit(X_scaled, y)            # retrain on new batch
        print(f"  Incremental update: {len(new_interactions)} new interactions")

    def predict(self, user_id: str, post_id: str) -> float:
        """Return P(user likes post) ∈ [0, 1]."""
        feat = make_features(user_id, post_id)
        feat_scaled = self.scaler.transform([feat])
        return float(self.model.predict_proba(feat_scaled)[0][1])

    def rank_posts(self, user_id: str, post_ids: list, top_k: int = 3) -> list:
        """Score all posts for a user, return top-K sorted by score."""
        scored = [(pid, self.predict(user_id, pid)) for pid in post_ids]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


if __name__ == "__main__":
    print("=== Model Training Demo ===\n")

    model = RecommendationModel()
    print("Full training on historical data:")
    model.fit(INTERACTIONS)

    print("\nRankings for each user (top 3 posts):")
    for uid, udata in USERS.items():
        top = model.rank_posts(uid, list(POSTS.keys()))
        scores = ", ".join(f"{pid}={s:.2f}" for pid, s in top)
        print(f"  {udata['name']:25s} → {scores}")
