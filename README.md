# Career Compass

A first usable version of a graduate career guidance web app. It combines an explainable rule-based expert component with TF-IDF text similarity over an included career knowledge base, then presents skill gaps, a learning roadmap, and a local assessment dashboard.

## Requirements and launch

Use Python 3.10 or later. From this folder, create and activate a virtual environment, then install dependencies and launch Streamlit:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If `py` is unavailable, install Python from python.org and ensure the launcher is on PATH. Open the local URL printed by Streamlit.

## What is included

- Profile assessment for study area, experience, demonstrable skills, interests, and work themes.
- Ten starter roles in `data/careers.json`, with skill tags, interests, relevant study areas, activities, and roadmap suggestions.
- Expert rules that score explicit profile overlap and show match reasons.
- scikit-learn TF-IDF and cosine similarity as a content-matching component.
- Hybrid ranking (65% rule score, 35% text similarity); these weights are prototype choices, not learned parameters.
- Role-specific skill-gap view, phased roadmap, and Plotly dashboard based on local SQLite assessment history.
- Tests for ranking/explanations and local persistence.

## Data provenance, evaluation, and limits

The included career descriptions and learning suggestions are starter content authored for this project; they are not an independently verified occupational taxonomy, live vacancy feed, or labor-market dataset. The text model is fitted at runtime on those descriptions, not on graduate profiles or outcomes. This workspace contains no labeled graduate outcome data, so predictive accuracy, fairness, and employment outcomes have not been evaluated. Scores are relative ranking aids and are not probabilities, aptitude assessments, or guarantees of employability. Review and replace the starter knowledge base with appropriately sourced, licensed, region-specific information before relying on it.

Profiles saved from the app are stored locally in `career_compass.db`. Avoid entering sensitive personal information. This prototype is for exploration and should not be used to make high-stakes decisions.

## Tests

```powershell
python -m pytest
```

The bundled desktop Python runtime can be used for inspection in this environment. For an actual deployment, install dependencies in an isolated Python environment as above.
