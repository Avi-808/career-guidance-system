# Career Compass

A first usable version of a graduate career guidance web app. It combines an explainable rule-based expert component with TF-IDF text similarity over an included career knowledge base, then presents skill gaps, a learning roadmap, and an assessment dashboard.

## Requirements and launch

Use Python 3.10 or later. From this folder, create and activate a virtual environment, then install dependencies and launch Streamlit:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If `py` is unavailable, install Python from [python.org](https://www.python.org/downloads/) and ensure the launcher is on PATH. Open the local URL printed by Streamlit.

## What is included

- Profile assessment for study area, experience, demonstrable skills, interests, and work themes.
- Ten starter roles in `data/careers.json`, with skill tags, interests, relevant study areas, activities, and roadmap suggestions.
- Expert rules that score explicit profile overlap and show match reasons.
- scikit-learn TF-IDF and cosine similarity as a content-matching component.
- Hybrid ranking (65% rule score, 35% text similarity); these weights are prototype choices, not learned parameters.
- Role-specific skill-gap view, phased roadmap, and Plotly dashboard based on SQLite assessment history.
- Tests for ranking/explanations and local persistence.

## Recommended project roadmap

These are suggested next steps; they are not all implemented yet.

- [ ] **Improve the career knowledge base:** expand role profiles with skills, tasks, education paths, outlook, sources, region, and last-updated dates. Use a suitable regional source, such as the [O*NET database](https://www.onetcenter.org/database.html) for U.S. occupation data or [ESCO occupations and skills](https://esco.ec.europa.eu/en/classification/occupation_main) for European occupation data. Check each source's coverage and license before importing it.
- [ ] **Make recommendations easier to evaluate:** show the skills and profile answers behind each match, let users compare roles, and keep scores clearly labeled as relative guidance rather than probabilities.
- [ ] **Add user-controlled profiles:** allow users to save, edit, and delete their profiles and results. Before hosting for multiple people, add authentication and ensure each user can access only their own records. See [Streamlit authentication](https://docs.streamlit.io/develop/concepts/connections/authentication).
- [ ] **Strengthen privacy:** collect only needed information, explain where it is stored, provide a clear delete/export option, and avoid asking for sensitive personal details.
- [ ] **Check quality and fairness:** test empty and incomplete profiles, ranking edge cases, storage isolation, and deletion. Review whether education or other profile choices skew recommendations; document what the checks can and cannot establish.
- [ ] **Improve the learning roadmap:** include practical projects, prerequisites, cost/accessibility notes, and links to learning resources; review links regularly.
- [ ] **Polish usability:** support mobile layouts, keyboard navigation, readable contrast, and clear explanations of how to use the tool.
- [ ] **Prepare deployment:** add a reproducible dependency lock or pinned environment, setup/deployment steps, and a smoke check for the hosted app.

## Data provenance, evaluation, and limits

The included career descriptions and learning suggestions are starter content authored for this project; they are not an independently verified occupational taxonomy, live vacancy feed, or labor-market dataset. The text model is fitted at runtime on those descriptions, not on graduate profiles or outcomes. This workspace contains no labeled graduate outcome data, so predictive accuracy, fairness, and employment outcomes have not been evaluated. Scores are relative ranking aids and are not probabilities, aptitude assessments, or guarantees of employability. Review and replace the starter knowledge base with appropriately sourced, licensed, region-specific information before relying on it.

When run locally, assessment records are stored in the SQLite database in this project directory. In a hosted deployment, that database is on the server and may be shared by app visitors unless user authentication and data isolation are added. Avoid entering sensitive personal information. This prototype is for exploration and should not be used to make high-stakes decisions.

## Tests

```powershell
python -m pytest
```

For an actual deployment, install dependencies in an isolated Python environment as above.
