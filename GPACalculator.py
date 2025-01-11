import streamlit as st

# =========================================
# 1. GPA Scales
# =========================================
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


# =========================================
# 2. Convert a numeric score (0–100) to a letter grade with decimal cutoffs
# =========================================
def score_to_letter(score: float) -> str:
    # Example decimal breakpoints
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


# =========================================
# 3. Weighted average for Chinese (3-part)
# =========================================
def get_chinese_points():
    st.write("Enter decimal scores (0–100) for each part:")
    c_score = st.number_input("Chinese (60%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)
    p_score = st.number_input("Native Politics (20%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)
    g_score = st.number_input("National Geography (20%) score", min_value=0.0, max_value=100.0, step=0.01, value=90.0)

    # Weighted average
    final_score = 0.6 * c_score + 0.2 * p_score + 0.2 * g_score
    # Convert to letter
    letter_grade = score_to_letter(final_score)
    st.write(f"**Weighted Score** = {final_score:.2f} → **Letter** = {letter_grade}")

    # Then convert letter -> numeric points (regular scale)
    points = letter_to_points(letter_grade, "regular")
    st.write(f"Chinese Culture => {points:.2f} points on 4.0 scale (Regular)")
    return points


# =========================================
# 4. Grade 10 and Grade 11 Curricula
# =========================================

# G10 required (except the “Elective” is optional)
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

# G11 required
# We remove "Honor Biology" so we can let the user pick it below
G11_BASE = [
    ("Chinese Culture 11", "regular", 0.5),
    ("AP World History", "advance", 1.0),
    # We'll insert an English option (Honor or AP) and a Biology option (Honor or AP)
    ("AP Science Elective", "advance", 1.0),
    ("AP Math Elective", "advance", 1.0),
    ("PE and Health 11", "regular", 0.5),
    ("PBL Research/AP Research", "advance", 0.5),
    ("PBL Track", "advance", 0.5),
]
G11_ELECTIVE = ("Elective (Optional)", "advance", 1.0)


# =========================================
# 5. GPA Calculation
# =========================================
def compute_gpa(courses_taken):
    total_qp = 0.0
    total_cr = 0.0
    for c in courses_taken:
        total_qp += c["actual_points"] * c["credits"]
        total_cr += c["credits"]
    if total_cr == 0:
        return 0.0, 0.0
    return (total_qp / total_cr), total_cr


# =========================================
# 6. Streamlit App
# =========================================
def main():
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

    # Gather user input for each course
    results = []
    for (cname, cdiff, ccredits) in base_courses:
        st.markdown("---")
        st.subheader(f"{cname} ({cdiff}, {ccredits} credits)")
        if "Chinese Culture" in cname:
            # Use the custom subgrades approach
            c_points = get_chinese_points()
            results.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": c_points
            })
        else:
            # Let user pick a letter grade
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

    # Compute GPA
    st.markdown("---")
    gpa, t_credits = compute_gpa(results)
    if t_credits == 0:
        st.warning("No valid credits, can't compute GPA.")
    else:
        st.success(f"**Your Weighted GPA** = {gpa:.2f} (Total Credits: {t_credits})")


if __name__ == "__main__":
    main()