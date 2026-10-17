"""Streamlit front end for the Career Compass hybrid guidance prototype."""
from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd

from career_engine import CareerEngine, load_careers, init_db, save_assessment, recent_assessments

ROOT = Path(__file__).parent
CAREERS = load_careers(ROOT / "data" / "careers.json")
ENGINE = CareerEngine(CAREERS)
init_db(ROOT / "career_compass.db")

st.set_page_config(page_title="Career Compass", page_icon="🧭", layout="wide")
st.title("🧭 Career Compass")
st.caption("A transparent career exploration prototype for graduates. Use results as a starting point for reflection, not as a hiring or aptitude verdict.")

with st.expander("Your graduate profile", expanded=True):
    st.caption("Select what you can demonstrate and what you enjoy. Your choices stay on this device.")
    with st.form("career_profile"):
        p1, p2 = st.columns(2)
        with p1:
            name = st.text_input("Name or nickname (optional)")
            education = st.selectbox("Study area", ["Computer Science / IT", "Engineering", "Business / Economics", "Natural Sciences", "Social Sciences", "Arts / Humanities", "Health / Life Sciences", "Other"])
            skill_options = sorted({s for c in CAREERS for s in c["skills"]})
            skills = st.multiselect("Skills you can demonstrate", skill_options, help="Choose skills you have used in coursework, projects, internships, or work.")
        with p2:
            interests = st.multiselect("Topics or activities you enjoy", sorted({i for c in CAREERS for i in c["interests"]}))
            work_style = st.multiselect("Preferred work themes", ["analytical", "creative", "collaborative", "independent", "people-focused", "structured", "fast-paced"])
        submitted = st.form_submit_button("Explore career matches", type="primary", use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["Career matches", "Skill gaps & roadmap", "Career knowledge base", "Dashboard & method"])

if submitted:
    result = ENGINE.recommend(skills, interests, education, work_style)
    st.session_state["result"] = result
    st.session_state["profile"] = {"name": name, "education": education, "skills": skills, "interests": interests, "work_style": work_style}
    save_assessment(ROOT / "career_compass.db", st.session_state["profile"], result)

with tab1:
    if "result" not in st.session_state:
        st.info("Fill in your profile above, then choose **Explore career matches**.")
    else:
        result = st.session_state["result"]
        st.subheader("Your strongest matches")
        st.caption("The combined score balances explicit rules and knowledge-base text similarity. Scores are relative ranking aids, not probabilities or job-market forecasts.")
        for ix, item in enumerate(result[:5], start=1):
            career = item["career"]
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"### {ix}. {career['title']}")
                c1.write(career["summary"])
                c2.metric("Hybrid score", f"{item['score']:.0f}/100")
                c1.markdown("**Why it matched:** " + ("; ".join(item["reasons"]) if item["reasons"] else "Broad match from the selected profile; explore the role details below."))
                c1.caption(f"Rule component {item['rule_score']:.0f}/100 · text similarity {item['text_score']:.0f}/100 · Evidence: curated role descriptions, not graduate outcome data")

with tab2:
    if "result" not in st.session_state:
        st.info("Explore matches first to see a tailored skills analysis and roadmap.")
    else:
        profile = st.session_state["profile"]
        target = st.selectbox("Build a plan for", [x["career"]["title"] for x in st.session_state["result"][:5]])
        item = next(x for x in st.session_state["result"] if x["career"]["title"] == target)
        missing = [s for s in item["career"]["skills"] if s not in profile["skills"]]
        c1, c2 = st.columns(2)
        c1.metric("Role skills already selected", f"{len(item['career']['skills']) - len(missing)} / {len(item['career']['skills'])}")
        c2.metric("Suggested areas to build", len(missing))
        st.markdown("#### Skill-gap view")
        skill_df = pd.DataFrame({"Skill": item["career"]["skills"], "Status": ["Have" if s in profile["skills"] else "Build" for s in item["career"]["skills"]]})
        st.dataframe(skill_df, hide_index=True, use_container_width=True)
        st.markdown("#### Suggested learning roadmap")
        for phase in item["career"]["roadmap"]:
            with st.expander(phase["phase"], expanded=True):
                st.write(phase["goal"])
                st.markdown("**Try:** " + phase["activity"])
                st.caption("Choose free or affordable resources that fit your location and schedule; this prototype does not verify course availability.")

with tab3:
    st.subheader("Curated career knowledge base")
    st.write("Role summaries, skill tags, interests, and roadmap suggestions below are starter content authored for this prototype. They are not sourced from live job postings or a labor-market database.")
    for c in CAREERS:
        with st.expander(c["title"]):
            st.write(c["summary"])
            st.markdown("**Common skills:** " + ", ".join(c["skills"]))
            st.markdown("**Related interests:** " + ", ".join(c["interests"]))
            st.markdown("**Typical activities:** " + c["activities"])

with tab4:
    st.subheader("Your local dashboard")
    history = recent_assessments(ROOT / "career_compass.db")
    if history.empty:
        st.info("No assessment history yet. Submit a profile to create the first local record.")
    else:
        st.metric("Saved assessments on this device", len(history))
        st.dataframe(history, hide_index=True, use_container_width=True)
        counts = history["Top match"].value_counts().rename_axis("Career").reset_index(name="Assessments")
        st.plotly_chart(px.bar(counts, x="Career", y="Assessments", title="Top match by saved assessment"), use_container_width=True)
    with st.expander("How the hybrid recommendations work"):
        st.markdown("""
        - **Rule-based expert component:** explicit overlap between selected skills, interests, education area, and work themes and the curated role profile. The interface shows matching reasons.
        - **ML component:** a scikit-learn TF-IDF vectorizer and cosine similarity compare the profile text with career descriptions in the included knowledge base. The model is fitted on those authored descriptions at startup; it is a content-matching aid, not a model trained on people.
        - **Hybrid ranking:** 65% rule score and 35% text similarity by default. This is a configurable design choice, not a learned or validated weight.
        - **Evaluation and provenance:** no labeled graduate outcomes or independently sourced benchmark data are included. Accuracy, fairness, and employment outcomes have not been measured. Do not interpret scores as probabilities.
        - **Privacy:** assessments are stored in a local SQLite file in this project directory. Do not enter sensitive personal information.
        """)
