import streamlit as st
import pandas as pd

# Load final DSS output
df = pd.read_csv("placements_dss_output.csv")

st.title("🎓 Career Decision Support System")
st.write("Interactive DSS to guide B.Tech students in career planning")

student_id = st.number_input(
    "Enter Student ID",
    min_value=1,
    step=1
)

if st.button("Get Career Recommendation"):

    student = df[df["Student ID"] == student_id]

    if student.empty:
        st.error("Student ID not found. Please enter a valid ID.")
    else:
        student = student.iloc[0]

        st.subheader("📊 Student Profile")
        st.write(f"**Skill Count:** {student['Skill_Count']}")
        st.write(f"**Experience Level:** {student['Experience_Level']}")
        st.write(f"**Academic Risk:** {student['Academic_Risk']}")
        st.write(f"**Placement Readiness:** {student['Placement_Readiness']}")

        st.subheader("✅ Recommended Career Options")

        options = (
            student["Recommended_Options"]
            .strip("[]")
            .replace("'", "")
            .split(",")
        )

        for opt in options:
            st.success(opt.strip())
