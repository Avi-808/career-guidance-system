"""Transparent rule + TF-IDF career ranking and local assessment storage."""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def load_careers(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class CareerEngine:
    def __init__(self, careers):
        self.careers = careers
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.career_matrix = self.vectorizer.fit_transform([self._career_text(c) for c in careers])

    @staticmethod
    def _career_text(c):
        return " ".join([c["title"], c["summary"], c["activities"], *c["skills"], *c["interests"], *c["education"]])

    def recommend(self, skills, interests, education, work_style):
        profile_text = " ".join([*skills, *interests, education, *work_style])
        if profile_text.strip():
            similarities = cosine_similarity(self.vectorizer.transform([profile_text]), self.career_matrix)[0]
        else:
            similarities = [0.0] * len(self.careers)
        results = []
        for career, sim in zip(self.careers, similarities):
            matched_skills = sorted(set(skills) & set(career["skills"]))
            matched_interests = sorted(set(interests) & set(career["interests"]))
            education_match = education in career["education"]
            style_match = sorted(set(work_style) & set(career["work_style"]))
            # Each criterion is inspectable. Denominator is fixed so scores remain comparable.
            rule = 100 * (0.55 * len(matched_skills) / max(1, len(career["skills"])) +
                          0.25 * len(matched_interests) / max(1, len(career["interests"])) +
                          0.12 * education_match +
                          0.08 * len(style_match) / max(1, len(career["work_style"])))
            text_score = float(sim) * 100
            score = 0.65 * rule + 0.35 * text_score
            reasons = []
            if matched_skills:
                reasons.append("matching skills: " + ", ".join(matched_skills))
            if matched_interests:
                reasons.append("matching interests: " + ", ".join(matched_interests))
            if education_match:
                reasons.append("study area is listed as relevant")
            if style_match:
                reasons.append("matching work themes: " + ", ".join(style_match))
            results.append({"career": career, "score": score, "rule_score": rule,
                            "text_score": text_score, "reasons": reasons})
        return sorted(results, key=lambda x: x["score"], reverse=True)


def init_db(path):
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, display_name TEXT,
            education TEXT, skills TEXT NOT NULL, interests TEXT NOT NULL,
            top_match TEXT NOT NULL, ranked_matches TEXT NOT NULL)""")


def save_assessment(path, profile, results):
    payload = [{"title": r["career"]["title"], "score": round(r["score"], 2)} for r in results[:5]]
    with sqlite3.connect(path) as conn:
        conn.execute("INSERT INTO assessments(created_at,display_name,education,skills,interests,top_match,ranked_matches) VALUES(?,?,?,?,?,?,?)",
                     (datetime.now(timezone.utc).isoformat(), profile.get("name", ""), profile["education"],
                      json.dumps(profile["skills"]), json.dumps(profile["interests"]), payload[0]["title"], json.dumps(payload)))


def recent_assessments(path):
    with sqlite3.connect(path) as conn:
        return pd.read_sql_query("SELECT created_at AS 'Saved (UTC)', display_name AS 'Name', education AS 'Study area', top_match AS 'Top match' FROM assessments ORDER BY id DESC LIMIT 100", conn)
