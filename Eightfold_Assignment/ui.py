import streamlit as st
import json
import tempfile

from app import run_pipeline, run_manual_pipeline
from validation import validate


# =========================
# CONFIG
# =========================

st.set_page_config("Profile Engine", layout="wide")

if "ready" not in st.session_state:
    st.session_state.ready = False

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "projected" not in st.session_state:
    st.session_state.projected = {}

if "custom" not in st.session_state:
    st.session_state.custom = {}


# =========================
# HEADER
# =========================

st.title("Multi-Source Candidate Data Transformer")


# =========================
# INPUT MODE
# =========================

# =========================
# INPUT MODE
# =========================

mode = st.radio(
    "Input Mode",
    [
        "Sample Data",
        "Manual Entry"
    ]
)

ats_file = None
linkedin_file = None

if mode == "Manual Entry":
    if mode == "Manual Entry":

        st.subheader(" ATS Data")

        ats_name = st.text_input("Candidate Name")
        ats_email = st.text_input("Email")
        ats_phone = st.text_input("Phone")

        ats_exp = st.number_input(
            "Experience (Years)",
            min_value=0,
            key="ats_exp"
        )

        ats_skills = st.text_area(
            "ATS Skills (comma separated)",
            key="ats_skills"
        )

        st.divider()

        st.subheader(" LinkedIn Data")

        linkedin_name = st.text_input(
            "LinkedIn Name"
        )

        linkedin_headline = st.text_input(
            "Headline"
        )

        linkedin_location = st.text_input(
            "Location"
        )

        linkedin_exp = st.number_input(
            "LinkedIn Experience",
            min_value=0,
            key="linkedin_exp"
        )

        linkedin_skills = st.text_area(
            "LinkedIn Skills (comma separated)",
            key="linkedin_skills"
        )


# =========================
# GENERATE
# =========================

if st.button(
    "Generate Profile",
    use_container_width=True
):

    try:

        # -------------------
        # SAMPLE DATA
        # -------------------

        if mode == "Sample Data":

            profile, projected, custom = run_pipeline()

        # -------------------
        # UPLOAD FILES
        # -------------------

        
        # -------------------
        # MANUAL ENTRY
        # -------------------

        elif mode == "Manual Entry":

            

            ats = {
                "full_name": ats_name,
                "emails": [ats_email] if ats_email else [],
                "phones": [ats_phone] if ats_phone else [],
                "years_experience": ats_exp,
                "skills": [
                    s.strip()
                    for s in ats_skills.split(",")
                    if s.strip()
                ]
            }

            linkedin = {
                "full_name": linkedin_name,
                "headline": linkedin_headline,
                "location": linkedin_location,
                "years_experience": linkedin_exp,
                "skills": [
                    s.strip()
                    for s in linkedin_skills.split(",")
                    if s.strip()
                ]
            }

            profile, projected, custom = run_manual_pipeline(
                ats,
                linkedin
            )

        st.session_state.profile = profile
        st.session_state.projected = projected
        st.session_state.custom = custom
        st.session_state.ready = True

        st.success(
            "Pipeline Complete "
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
            )


# =========================
# DASHBOARD
# =========================

st.divider()

p = st.session_state.profile

c1, c2, c3, c4 = st.columns(4)

c1.metric("Name", p.get("full_name", "-"))
c2.metric("Experience", p.get("years_experience", "-"))
c3.metric("Skills", len(p.get("skills", [])))
c4.metric("Confidence", f"{int(p.get('overall_confidence',0)*100)}%")


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4= st.tabs(["Outputs", "Validation","Provenance", "Gold Check"])


# =========================
# TAB 1
# =========================

with tab1:

    if not st.session_state.ready:
        st.info("Generate profile first")

    else:

        profile = st.session_state.profile
        st.json(profile)
        # =====================================
        # CANONICAL PROFILE
        # =====================================

        st.subheader(" Canonical Profile (Default Schema)")

        st.json(profile)

        
        # =====================================
        # PROVENANCE TRACKING
        # =====================================

        

        # =====================================
        # CONFIG OUTPUT
        # =====================================

        st.divider()

        st.subheader(
            " Config Driven Projection Output"
        )

        st.json(
            st.session_state.projected
        )

        # =====================================
        # CUSTOM OUTPUT
        # =====================================

        st.divider()

        st.subheader(
            " Projection Output"
        )

        st.json(
            st.session_state.custom
        )

       
st.subheader("⬇ Download Outputs")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="Download Canonical Profile",
        data=json.dumps(
            st.session_state.profile,
            indent=4
        ),
        file_name="canonical_profile.json",
        mime="application/json"
    )

with col2:
    st.download_button(
        label="Download Projected Output",
        data=json.dumps(
            st.session_state.projected,
            indent=4
        ),
        file_name="projected_output.json",
        mime="application/json"
    )

with col3:
    st.download_button(
        label="Download Custom Output",
        data=json.dumps(
            st.session_state.custom,
            indent=4
        ),
        file_name="custom_output.json",
        mime="application/json"
    )
# =========================
# TAB 2
# =========================

with tab2:

    if not st.session_state.ready:
        st.info("No validation yet")
    else:

        checks = validate(st.session_state.profile)

        score = 0

        for name, ok in checks:
            if ok:
                st.success(name)
                score += 1
            else:
                st.error(name)

        st.metric("Validation Score", f"{score}/{len(checks)}")


# =========================
# TAB 3
# =========================
with tab3:

    if not st.session_state.ready:
        st.info("Generate profile first")

    else:

        st.subheader("Field Lineage")

        rows = []

        for field, info in st.session_state.profile["provenance"].items():

            rows.append({
                "Field": field,
                "Source": info.get("source"),
                "Method": info.get("method"),
                "Confidence": info.get("confidence", "-")
            })

        st.dataframe(
            rows,
            use_container_width=True
        )

with tab4:

    if not st.session_state.ready:
        st.info("Generate profile first")
    else:

        with open("tests/gold_profile.json") as f:
            gold = json.load(f)

        p = st.session_state.profile

        rows = []
        match = 0

        for k in gold:
            ok = gold[k] == p.get(k)
            match += int(ok)

            rows.append({
                "Field": k,
                "Expected": gold[k],
                "Actual": p.get(k),
                "Match": "✅" if ok else "❌"
            })

        st.dataframe(rows)
        st.metric("Match %", f"{round(match/len(gold)*100,2)}%")


    