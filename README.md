# Career Decision Support System (DSS)

## Problem Statement
Many B.Tech students face confusion while choosing an appropriate career path after graduation. Due to multiple available options such as jobs, higher studies, skill development, or waiting to improve profiles, students often make decisions based on peer influence or incomplete information. This project aims to build a Decision Support System (DSS) that provides data-driven career guidance based on student academic performance, skills, and experience.

---

## Project Overview
The Career Decision Support System analyzes student profiles and suggests suitable career options instead of forcing a single decision. The system evaluates multiple indicators and presents ranked career recommendations to support informed decision-making.

The recommended career options include:
- Immediate Job
- Higher Studies
- Skill Improvement
- Wait & Improve

---

## Project Workflow
1. Data Cleaning  
   The raw placement dataset was cleaned by removing unnecessary attributes and preparing the data for analysis.

2. Feature Engineering  
   New features were created such as:
   - Skill Count
   - Experience Level
   - Academic Risk
   - Placement Readiness

3. DSS Logic Implementation  
   A rule-based scoring mechanism was used to evaluate multiple career alternatives based on student profiles.

4. Interface Development  
   A Streamlit-based interactive interface was developed to demonstrate the DSS recommendations.

---

## Technologies Used
- Python  
- Pandas  
- Jupyter Notebook  
- Streamlit  
- VS Code  

---

## How to Run the Project
1. Install Streamlit:
   pip install streamlit

2. Run the application:
   streamlit run app.py


---

## Output
The system displays the student profile summary along with recommended career options based on the DSS evaluation. The recommendations support decision-making rather than enforcing a single career choice.

---

## Note
Student identities were anonymized to ensure privacy and ethical data usage.


