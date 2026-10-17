import json
from pathlib import Path
from career_engine import CareerEngine, init_db, save_assessment, recent_assessments

DATA = Path(__file__).parents[1] / "data" / "careers.json"


def test_recommendations_are_ranked_and_explainable():
    careers = json.loads(DATA.read_text(encoding="utf-8"))
    results = CareerEngine(careers).recommend(["SQL", "Python"], ["data"], "Computer Science / IT", ["analytical"])
    assert len(results) == len(careers)
    assert results[0]["career"]["title"] == "Data Analyst"
    assert results[0]["reasons"]
    assert all(0 <= r["score"] <= 100 for r in results)


def test_local_assessment_storage(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    save_assessment(db, {"name":"Test", "education":"Other", "skills":[], "interests":[]},
                    [{"career":{"title":"Role"}, "score":42.5}])
    frame = recent_assessments(db)
    assert len(frame) == 1
    assert frame.iloc[0]["Top match"] == "Role"
    assert "Top match" in frame.columns
