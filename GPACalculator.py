import streamlit as st

# -----------------------------------------
# 1. Letter-grade -> numeric mappings
# -----------------------------------------
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


# -----------------------------------------
# 2. A function to convert a letter grade
#    and difficulty -> numeric GPA points
# -----------------------------------------
def letter_to_points(letter_grade: str, difficulty: str) -> float:
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


# -----------------------------------------
# 3. Convert numeric score (0–100) -> letter grade
#    You can adjust these thresholds as needed.
# -----------------------------------------
def score_to_letter(score: float) -> str:
    """
    Convert a numeric score (0–100) to a letter grade,
    using decimal thresholds per your requirement.
    E.g., >=92.5 => A, >=88.5 => A-, etc.
    """

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


# -----------------------------------------
# 4. Course lists
#    - All are required except for ONE elective
# -----------------------------------------
G10_BASE = [
    ("Chinese Culture 10", "regular", 0.5),
    ("HAG (History&Geog)", "honor", 1.0),
    ("English 10", "honor", 1.0),
    ("Chemistry", "honor", 1.0),
    ("Physics1", "advance", 1.0),
    ("Pre-calculus", "advance", 1.0),
    ("PE", "regular", 0.5),
    ("PBL Core", "advance", 0.5),
    ("PBL AI", "advance", 0.5),
]
G10_ELECTIVE = ("Elective (Optional)", "advance", 1.0)

G11_BASE = [
    ("Chinese 11", "regular", 0.5),
    ("World History", "advance", 1.0),
    ("Honor English", "honor", 0.5),
    ("AP English", "advance", 0.5),
    ("Biology", "advance", 1.0),
    ("Chemistry", "advance", 1.0),
    ("Statistics", "advance", 1.0),
    ("PE", "regular", 0.5),
    ("PBL IR", "advance", 0.5),
    ("PBL AI", "advance", 0.5),
]
G11_ELECTIVE = ("Elective (Optional)", "advance", 1.0)


# -----------------------------------------
# 5. GPA Calculation
# -----------------------------------------
def calculate_gpa(courses):
    """
    courses is a list of dicts, each with:
        name, difficulty, credits,
        actual_points (the GPA points),
    We'll do sum(actual_points * credits) / sum(credits)
    """
    total_quality_points = 0.0
    total_credits = 0.0

    for c in courses:
        total_quality_points += c["actual_points"] * c["credits"]
        total_credits += c["credits"]

    if total_credits == 0:
        return 0.0, 0.0
    gpa = total_quality_points / total_credits
    return gpa, total_credits


# -----------------------------------------
# 6. Streamlit App
# -----------------------------------------
def main():
    st.title("Revised GPA Calculator")

    st.write("""
    **Instructions**:
    1. Choose Grade 10 or 11.
    2. Decide whether you take the optional Elective or not.
    3. For Chinese, **input numeric scores** (0–100).
       The app will convert that weighted average into a letter grade automatically.
    4. For other courses, pick a letter grade from the dropdown.
    5. A final credit-weighted GPA is displayed.
    """)

    # Grade selection
    year_choice = st.radio("Select your grade:", ["Grade 10", "Grade 11"])

    if year_choice == "Grade 10":
        course_base = list(G10_BASE)
        elective_course = G10_ELECTIVE
    else:
        course_base = list(G11_BASE)
        elective_course = G11_ELECTIVE

    # Option to add elective or not
    add_elective = st.checkbox("Add Elective?", value=False)
    if add_elective:
        course_base.append(elective_course)

    # We'll build a data structure
    # to store actual_points for each course
    computed_courses = []

    # Go through each course
    for (cname, cdiff, ccredits) in course_base:
        st.markdown("---")
        st.subheader(f"{cname} - {cdiff} - {ccredits} credits")

        if "Chinese" in cname:
            # Instead of selecting a letter grade,
            # user inputs numeric score for sub-parts
            st.write("**Please enter your numeric scores (0–100) for each sub-part**:")
            c_score = st.number_input("Chinese (60%) score:", min_value=0, max_value=100, value=90, step=1,
                                      key=f"{cname}_CH")
            p_score = st.number_input("Politics (20%) score:", min_value=0, max_value=100, value=90, step=1,
                                      key=f"{cname}_PO")
            g_score = st.number_input("Geography (20%) score:", min_value=0, max_value=100, value=90, step=1,
                                      key=f"{cname}_GE")

            # Weighted average
            final_score = 0.6 * c_score + 0.2 * p_score + 0.2 * g_score
            # Convert numeric (0–100) -> letter
            c_letter = score_to_letter(final_score)
            st.write(f"Calculated weighted score: **{final_score:.1f}** → Letter grade: **{c_letter}**")

            # Now convert letter to GPA points (regular scale)
            actual_points = letter_to_points(c_letter, "regular")
            st.write(f"GPA Points (Regular scale): **{actual_points:.2f}**")

            computed_courses.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": actual_points
            })
        else:
            # For other courses, pick letter from dropdown
            letter_choice = st.selectbox(
                f"Letter Grade for {cname}",
                options=list(regular_scale.keys()),
                key=cname  # unique key
            )
            # Convert letter -> numeric
            actual_points = letter_to_points(letter_choice, cdiff)
            st.write(f"GPA Points: **{actual_points:.2f}**")

            computed_courses.append({
                "name": cname,
                "difficulty": cdiff,
                "credits": ccredits,
                "actual_points": actual_points
            })

    # Calculate final GPA
    gpa, total_credits = calculate_gpa(computed_courses)

    st.markdown("---")
    st.header("Final Results")
    if total_credits == 0:
        st.warning("No valid credits. Cannot compute GPA.")
    else:
        st.success(f"**Weighted GPA**: {gpa:.2f}  (Total Credits: {total_credits})")


if __name__ == "__main__":
    main()