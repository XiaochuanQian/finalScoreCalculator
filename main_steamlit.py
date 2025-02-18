import streamlit as st
from datetime import datetime

# ----------------------------- Existing Functions -----------------------------

# Function to calculate the required final exam score
def calculate_final_exam_score(current_score, desired_score, final_weight):
    """
    Calculate the score needed on the final exam to achieve the desired overall grade.
    """
    final_weight /= 100
    needed_score = (desired_score - (current_score * (1 - final_weight))) / final_weight
    return needed_score

# Function for love calculator
def love_calculator(name1, name2):
    """Calculate a compatibility score based on two names."""
    combined_names = name1 + name2
    total = 0
    for char in combined_names.upper():
        if char.isalpha():
            total += ord(char) - ord('A') + 1
    love_score = total % 101
    return love_score

# Function to check if the current date is Valentine's Day or Qixi Festival
def is_special_day():
    today = datetime.now()
    # Valentine's Day: February 14
    if today.month == 2 and today.day == 14:
        return True
    # Qixi Festival (approximation): August 7
    if today.month == 8 and today.day == 7:
        return True
    return False

# ---------------------------- GPA Calculator Functions ----------------------------

# GPA Scales
regular_scale = {
    "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}

honor_scale = {
    "A": 4.5, "A-": 4.2,
    "B+": 3.8, "B": 3.5, "B-": 3.2,
    "C+": 2.8, "C": 2.5, "C-": 2.2,
    "D+": 1.8, "D": 1.5, "F": 0.0
}

advance_scale = {
    "A": 5.0, "A-": 4.7,
    "B+": 4.3, "B": 4.0, "B-": 3.7,
    "C+": 3.3, "C": 3.0, "C-": 2.7,
    "D+": 2.3, "D": 2.0, "F": 0.0
}

def letter_to_points(letter_grade: str, difficulty: str) -> float:
    """Convert letter grade (A,B+,etc.) + difficulty into numeric points."""
    lg = letter_grade.upper().strip()
    diff = difficulty.lower().strip()

    if diff == "regular":
        return regular_scale.get(lg, 0.0)
    elif diff == "honor":
        return honor_scale.get(lg, 0.0)
    elif diff in ["advance", "advanced", "ap"]:
        return advance_scale.get(lg, 0.0)
    else:
        return regular_scale.get(lg, 0.0)

def score_to_letter(score: float) -> str:
    if score >= 92.5:
        return "A"
    elif score >= 88.5:
        return "A-"
    elif score >= 84.5:
        return "B+"
    elif score >= 80.5:
        return "B"
    elif score >= 77.5:
        return "B-"
    elif score >= 74.5:
        return "C+"
    elif score >= 70.5:
        return "C"
    elif score >= 67.5:
        return "C-"
    elif score >= 64.5:
        return "D+"
    elif score >= 60.0:
        return "D"
    else:
        return "F"

def get_chinese_points():
    st.write("Enter decimal scores (0–100) for each part:")
    c_score = st.number_input("Chinese (60%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)
    p_score = st.number_input("Native Politics (20%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)
    g_score = st.number_input("National Geography (20%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)

    final_score = 0.6 * c_score + 0.2 * p_score + 0.2 * g_score
    letter_grade = score_to_letter(final_score)
    st.write(f"**Weighted Score** = {final_score:.2f} → **Letter** = {letter_grade}")

    points = letter_to_points(letter_grade, "regular")
    st.write(f"Chinese Culture => {points:.2f} points on 4.0 scale (Regular)")
    return points

def get_chinese_points_g11():
    st.write("Enter decimal scores (0–100) for each part:")
    c_score = st.number_input("Chinese (75%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)
    gp_score = st.number_input("Geo/Politics (25%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)

    final_score = 0.75 * c_score + 0.25 * gp_score
    letter_grade = score_to_letter(final_score)
    st.write(f"**Weighted Score** = {final_score:.2f} → **Letter** = {letter_grade}")

    points = letter_to_points(letter_grade, "regular")
    st.write(f"Chinese Culture (G11) => {points:.2f} points on 4.0 scale (Regular)")
    return points


# Course data for GPA Calculator
G10_BASE = [
    ("Chinese Culture 10", "regular", 0.5),
    ("History and Geography", "honor", 1.0),
    ("Honor English/English 10", "honor", 1.0),
    ("Honor Chemistry", "honor", 1.0),
    ("Honor Physics/AP Physics 1", "advance", 1.0),
    ("Algebra 2/AP Pre-calculus", "advance", 1.0),
    ("PE and Health 10", "regular", 0.5),
    ("PBL Core/AP Seminar", "advance", 0.5),
    ("PBL Track", "advance", 0.5),
]
G10_ELECTIVE = ("Elective (Optional)", "advance", 1.0)

G11_BASE = [
    ("Chinese Culture 11", "regular", 0.5),
    ("AP World History", "advance", 1.0),
    # placeholders for English and Biology courses will be inserted dynamically
    ("AP Science Elective", "advance", 1.0),
    ("AP Math Elective", "advance", 1.0),
    ("PE and Health 11", "regular", 0.5),
    ("PBL Research/AP Research", "advance", 0.5),
    ("PBL Track", "advance", 0.5),
]
G11_ELECTIVE = ("Elective (Optional)", "advance", 1.0)

def compute_gpa(courses_taken):
    total_qp = 0.0
    total_cr = 0.0
    for c in courses_taken:
        total_qp += c["actual_points"] * c["credits"]
        total_cr += c["credits"]
    if total_cr == 0:
        return 0.0, 0.0
    return (total_qp / total_cr), total_cr

def run_gpa_calculator():
    st.title("High School GPA Calculator (With Biology Options)")

    st.write("""
    **Instructions**:
    1. Select Grade 10 or 11.
    2. Decide if you want the optional Elective.
    3. For G11, pick your English course (Honor or AP) **and** your Biology course (Honor or AP).
    4. For Chinese Culture, input your decimal scores.
    5. For other courses, choose letter grades.
    6. Final GPA is credit-weighted.
    """)

    grade = st.radio("Which grade are you calculating?", ["Grade 10", "Grade 11"])

    if grade == "Grade 10":
        base_courses = list(G10_BASE)
        elective = G10_ELECTIVE
    else:
        base_courses = list(G11_BASE)
        elective = G11_ELECTIVE

        # -- G11 English Option --
        eng_choice = st.radio("English Course (G11):", ["Honor English", "AP English"])
        if eng_choice == "Honor English":
            base_courses.insert(2, ("Honor English (G11)", "honor", 1.0))
        else:
            base_courses.insert(2, ("AP English (G11)", "advance", 1.0))

        # -- G11 Biology Option --
        bio_choice = st.radio("Biology Course (G11):", ["Honor Biology", "AP Biology"])
        if bio_choice == "Honor Biology":
            base_courses.insert(3, ("Honor Biology (G11)", "honor", 1.0))
        else:
            base_courses.insert(3, ("AP Biology (G11)", "advance", 1.0))

    # Optional Elective
    take_elective = st.checkbox("Add the Elective?", value=False)
    if take_elective:
        base_courses.append(elective)

    results = []
    for (cname, cdiff, ccredits) in base_courses:
        st.markdown("---")
        st.subheader(f"{cname} ({cdiff}, {ccredits} credits)")
        if "Chinese Culture 10" in cname:
            c_points = get_chinese_points()
            results.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": c_points
            })
        elif "Chinese Culture 11" in cname:
            c_points = get_chinese_points_g11()  # 使用新的 G11 计算函数
            results.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": c_points
            })
        else:
            letter_choice = st.selectbox(
                f"Letter Grade for {cname}",
                options=list(regular_scale.keys()),
                key=cname
            )
            numeric = letter_to_points(letter_choice, cdiff)
            st.write(f"GPA Points: {numeric:.2f}")
            results.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": numeric
            })

    st.markdown("---")
    gpa, t_credits = compute_gpa(results)
    if t_credits == 0:
        st.warning("No valid credits, can't compute GPA.")
    else:
        st.success(f"**Your Weighted GPA** = {gpa:.3f} (Total Credits: {t_credits})")


# ---------------------------- Streamlit App Layout ----------------------------

st.set_page_config(page_title="Multi-Feature App", page_icon="💡")

# Sidebar navigation
st.sidebar.title("Navigation")

# Determine available pages
available_pages = ["Final Exam Score Calculator", "GPA Calculator"]
if is_special_day():
    available_pages.append("Love Calculator")

page = st.sidebar.radio("Select a feature:", available_pages)

if page == "Final Exam Score Calculator":
    st.title('Final Exam Score Calculator')

    tab1, tab2 = st.tabs(["Use Sliders", "Type Values"])

    current_score = 92.5
    desired_score = 90.0
    final_weight = 40.0

    with tab1:
        st.write("Use sliders to set the values:")
        current_score = st.slider('Current Overall Score (%)', 0.0, 100.0, current_score, 0.01)
        desired_score = st.slider('Desired Overall Score (%)', 0.0, 100.0, desired_score, 0.01)
        final_weight = st.slider('Final Exam Weight (%)', 0.0, 100.0, final_weight, 0.5)

    with tab2:
        st.write("Type the values directly:")
        current_score_input = st.text_input("Enter Current Overall Score (%)", str(current_score))
        desired_score_input = st.text_input("Enter Desired Overall Score (%)", str(desired_score))
        final_weight_input = st.text_input("Enter Final Exam Weight (%)", str(final_weight))

        try:
            current_score = float(current_score_input)
            desired_score = float(desired_score_input)
            final_weight = float(final_weight_input)
        except ValueError:
            st.error("Please enter valid numeric values.")

    if st.button('Calculate Required Final Score'):
        if current_score is not None and desired_score is not None and final_weight is not None:
            if 0 <= current_score <= 100 and 0 <= desired_score <= 100 and 0 <= final_weight <= 100:
                needed_score = calculate_final_exam_score(current_score, desired_score, final_weight)
                if 0 <= needed_score <= 100:
                    st.write(f"You need to score **{needed_score:.2f}%** on the final exam to achieve your desired overall score.")
                elif needed_score < 0:
                    st.write("Congratulations! You have already achieved your desired score.")
                else:
                    st.write("It is not possible to achieve your desired score with the given final exam weight.")
            else:
                st.error("Please ensure all inputs are between 0 and 100.")
        else:
            st.error("Missing or invalid inputs. Please check your values.")

elif page == "Love Calculator":
    st.title('Love Calculator')

    name1 = st.text_input("Enter the first name:", "Alice")
    name2 = st.text_input("Enter the second name:", "Bob")

    if st.button('Calculate Love Score'):
        if name1 and name2:
            score = love_calculator(name1, name2)
            st.write(f"The love score between **{name1}** and **{name2}** is: **{score}%**")
        else:
            st.error("Please enter both names.")

elif page == "GPA Calculator":
    run_gpa_calculator()
