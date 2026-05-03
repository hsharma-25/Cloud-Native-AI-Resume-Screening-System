import streamlit as st
import pandas as pd

from utils.pdf_parser import extract_text_from_pdf
from utils.preprocessing import clean_text
from utils.ranking import rank_resumes


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="wide"
)

def load_css():
    with open("styles/main.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------


def get_fit_label(score):
    score = score*100

    if score >= 60:
        return "🟢 Strong Match", "strong"
    elif score >= 40:
        return "🟡 Moderate Match", "moderate"
    else:
        return "🔴 Weak Match", "weak"


def generate_skill_table(result):

    rows = []

    matched = set(result["matched_skills"])
    missing = set(result["missing_skills"])

    all_skills = list(matched.union(missing))

    for skill in all_skills:

        if skill in matched:
            status = "✅ Match"
        else:
            status = "❌ Missing"

        rows.append({
            "Skill": skill.title(),
            "Status": status
        })

    return rows


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    """
    <div>
        <div class='main-title'>📄 ResumeIQ</div>
        <div class='subtitle'>
            Intelligent resume ranking using semantic similarity and skill analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <h1 style='color:white;'>
            📊 Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <div style='color:#94a3b8'>
        AI-powered resume screening and ranking system
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Model Information")

    st.info("SBERT: all-MiniLM-L6-v2")

    st.info("Hybrid Matching")

    st.info("Semantic + Skill Analysis")

    st.markdown("---")

    if "results" in locals():

        st.markdown("---")

        st.markdown("### 📈 Live Analysis")

        st.metric(
            "Total Resumes",
            len(results)
        )

        st.metric(
            "Top Match Score",
            f"{top_score * 100:.1f}%"
        )

        st.metric(
            "Average Match Score",
            f"{average_score * 100:.1f}%"
        )


# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

# st.markdown("<div class='upload-box'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    jd_file = st.file_uploader(
        "Upload Job Description (PDF)",
        type="pdf"
    )

with col2:
    resume_files = st.file_uploader(
        "Upload Resumes (PDFs)",
        type="pdf",
        accept_multiple_files=True
    )



# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("🚀 Analyze Candidates"):

    if not jd_file or not resume_files:
        st.warning("Please upload both JD and resumes.")

    else:

        with st.spinner("Analyzing resumes..."):

            jd_text = extract_text_from_pdf(jd_file)
            jd_text = clean_text(jd_text)

            resumes = {}

            for file in resume_files:
                text = extract_text_from_pdf(file)
                text = clean_text(text)
                resumes[file.name] = text

            results = rank_resumes(jd_text, resumes)

            top_score = max(result["score"] for result in results)
            average_score = (
                sum(result["score"] for result in results)
                / len(results)
            )


        st.success("Analysis Complete")


        # ---------------------------------------------------
        # RESULTS
        # ---------------------------------------------------

        st.markdown("## 🏆 Ranked Candidates")


        for index, result in enumerate(results):
            
            is_best = index == 0

            label, label_class = get_fit_label(result["score"])

            with st.container():

                # if index == 0:
                #     # st.markdown("<div class='best-match-card'>", unsafe_allow_html=True)

                #     st.markdown(
                #         "<div class='best-badge'>🏆 Best Match</div>",
                #         unsafe_allow_html=True
                #     )

                st.markdown(
                    f"## {index+1}. {result['name']}"
                )

                st.markdown(
                    f"""
                    <div class='score-badge {label_class} glass-card'>
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # SCORE BAR
            st.progress(float(result["score"]))


            # METRICS
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-box glass-card">
                    <div class="metric-label">Final Score</div>
                    <div class="metric-value">{(result['score']*100):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-box glass-card">
                    <div class="metric-label">Semantic Match</div>
                    <div class="metric-value">{(result['semantic_score']*100):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-box glass-card">
                    <div class="metric-label">Skill Match</div>
                    <div class="metric-value">{(result['skill_score']*100):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)


            st.markdown("<br>", unsafe_allow_html=True)


            # MATCHED SKILLS
            st.markdown("### ✅ Matched Skills")

            matched_html = ""

            for skill in result["matched_skills"]:
                matched_html += (
                    f"<span class='skill-tag matched'>{skill}</span>"
                )

            st.markdown(matched_html, unsafe_allow_html=True)


            # MISSING SKILLS
            st.markdown("### ❌ Missing Skills")

            missing_html = ""

            for skill in result["missing_skills"]:
                missing_html += (
                    f"<span class='skill-tag missing'>{skill}</span>"
                )

            st.markdown(missing_html, unsafe_allow_html=True)


            st.markdown("### 📊 Skill Match Overview")

            skill_rows = generate_skill_table(result)

            df = pd.DataFrame(skill_rows)

            styled_df = df.style \
                .set_properties(**{
                    'background-color': '#111827',
                    'color': 'white',
                    'border-color': '#1f2937',
                    'font-size': '14px'
                }) \
                .set_table_styles([
                    {
                        'selector': 'th',
                        'props': [
                            ('background-color', '#1e293b'),
                            ('color', 'white'),
                            ('font-weight', 'bold'),
                            ('border', '1px solid #374151')
                        ]
                    }
                ])

            st.table(styled_df)


            # INSIGHTS
            st.markdown("### 💡 Resume Improvement Insights")

            for suggestion in result["suggestions"]:
                st.markdown(
                    f"""
                    <div class='insight-box glass-card'>
                        {suggestion}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            st.markdown("<br>", unsafe_allow_html=True)
